# components/diagnostics.py
# ─────────────────────────────────────────────────────────────────
# Diagnostics tab — the core UI:
#   1. Disease selector (pill tabs)
#   2. Input method: Manual form OR PDF upload
#   3. Dynamic form (built from constants.py)
#   4. Predict button → results panel
#   5. Download report button
# ─────────────────────────────────────────────────────────────────

import streamlit as st
import uuid
from datetime import datetime

from utils.constants    import DISEASE_META, DISEASE_FEATURES
from utils.predictor    import predict_disease, get_loaded_models
from utils.validators   import validate_patient_data
from components.report  import generate_report_pdf


# ═══════════════════════════════════════════════════════════════════
def render_diagnostics():
    """Render the full Diagnostics tab."""

    st.markdown(
        "<h2 style='color:#00B4D8;margin-bottom:0.2rem;'>🔬 Disease Diagnostics</h2>"
        "<p style='color:#8899AA;margin-top:0;'>Fill in lab values or upload a PDF report "
        "to get an AI-assisted risk assessment.</p>",
        unsafe_allow_html=True,
    )

    # ── Disease selector ──────────────────────────────────────────
    st.markdown("**Select Disease to Screen For**")

    disease_keys   = list(DISEASE_META.keys())
    disease_labels = [f"{DISEASE_META[d]['icon']} {DISEASE_META[d]['label']}"
                      for d in disease_keys]

    selected_idx = st.radio(
        label=" ",
        options=range(len(disease_keys)),
        format_func=lambda i: disease_labels[i],
        horizontal=True,
        key="disease_selector",
        label_visibility="collapsed",
    )

    selected_disease = disease_keys[selected_idx]
    meta             = DISEASE_META[selected_disease]

    # Show disease banner
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, {meta['color']}15 0%, transparent 100%);
        border-left: 4px solid {meta['color']};
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1.2rem;
        margin: 0.8rem 0 1.2rem 0;
    ">
        <span style="font-size:1.3rem;">{meta['icon']}</span>
        <strong style="color:#E0E6F0; margin-left:0.5rem;">{meta['label']}</strong>
        <span style="color:#8899AA; font-size:0.88rem; margin-left:0.5rem;">
            — {meta['description']}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Patient info row ──────────────────────────────────────────
    st.markdown("##### 👤 Patient Information")
    pi_col1, pi_col2, pi_col3 = st.columns(3)
    with pi_col1:
        patient_name = st.text_input(
            "Patient Name", value="", placeholder="Optional",
            help="Used in the downloadable report only.",
        )
    with pi_col2:
        patient_age_form = st.number_input(
            "Age (for report)", min_value=0, max_value=130,
            value=0, step=1,
            help="Age for the report header (separate from model features).",
        )
    with pi_col3:
        patient_gender_form = st.selectbox(
            "Gender (for report)",
            options=["", "Male", "Female", "Other / Prefer not to say"],
            help="Gender for the report header.",
        )

    st.divider()

    # ── Input method toggle ────────────────────────────────────────
    st.markdown("##### 📥 Input Method")
    input_method = st.radio(
        "How would you like to enter data?",
        options=["✍️ Manual Entry", "📄 Upload Lab Report PDF"],
        horizontal=True,
        key=f"input_method_{selected_disease}",
        label_visibility="collapsed",
    )

    # ── PDF Upload path ────────────────────────────────────────────
    prefilled_from_pdf: dict = {}
    pdf_warnings: list[str]  = []

    if "Upload" in input_method:
        st.markdown(
            "<p style='color:#8899AA;font-size:0.88rem;'>"
            "Upload your lab report PDF and the system will attempt to auto-extract "
            "values. You can review and correct any field before predicting."
            "</p>",
            unsafe_allow_html=True,
        )

        uploaded_pdf = st.file_uploader(
            "Upload PDF lab report",
            type=["pdf"],
            key=f"pdf_upload_{selected_disease}",
            help="Accepted: standard lab report PDFs. Scanned/image PDFs may not extract well.",
        )

        if uploaded_pdf is not None:
            with st.spinner("Extracting values from PDF…"):
                try:
                    from components.pdf_extractor import extract_fields, get_dummy_extracted
                    pdf_bytes         = uploaded_pdf.read()
                    prefilled_from_pdf = extract_fields(pdf_bytes, selected_disease)

                    # Fallback to dummy extraction if real extraction returns nothing
                    if not prefilled_from_pdf:
                        prefilled_from_pdf = get_dummy_extracted(selected_disease)
                        st.info(
                            "ℹ️ Real PDF extraction found no values in this file. "
                            "Pre-filling with demo values so you can see the form. "
                            "Please review and correct all fields.",
                        )
                    else:
                        n = len(prefilled_from_pdf)
                        st.success(f"✅ Extracted **{n}** values from PDF. "
                                   "Review the form below before predicting.")
                except Exception as e:
                    st.error(f"PDF extraction error: {e}")

        st.markdown("---")

    # ── Dynamic form ──────────────────────────────────────────────
    st.markdown(f"##### 🧪 Clinical Parameters — {meta['label']}")

    loaded_models   = get_loaded_models()
    model_available = selected_disease in loaded_models

    if not model_available:
        st.info(
            f"⚠️ **Demo Mode:** `{selected_disease}_model.pkl` not found in `models/`. "
            "Predictions will use a placeholder model. Results are illustrative only.",
            icon="🔧",
        )

    fields     = DISEASE_FEATURES.get(selected_disease, [])
    form_data  = {}

    # Layout: 2-column grid for wide screens
    field_chunks = [fields[i:i+2] for i in range(0, len(fields), 2)]

    with st.form(key=f"diagnostic_form_{selected_disease}"):
        for chunk in field_chunks:
            cols = st.columns(len(chunk))
            for col, field in zip(cols, chunk):
                with col:
                    key   = field["key"]
                    label = field["label"]
                    unit  = field.get("unit", "")
                    help_ = field.get("help", "")
                    ftype = field["type"]

                    display_label = f"{label} ({unit})" if unit else label
                    pdf_val       = prefilled_from_pdf.get(key)

                    if ftype == "number":
                        default = float(pdf_val) if pdf_val is not None else float(field.get("default", 0))
                        form_data[key] = st.number_input(
                            display_label,
                            min_value=float(field.get("min", 0)),
                            max_value=float(field.get("max", 9999)),
                            value=default,
                            step=float(field.get("step", 0.1)),
                            help=help_,
                            key=f"{selected_disease}_{key}",
                        )

                    elif ftype == "slider":
                        default = int(pdf_val) if pdf_val is not None else int(field.get("default", field.get("min", 0)))
                        form_data[key] = st.slider(
                            display_label,
                            min_value=int(field.get("min", 0)),
                            max_value=int(field.get("max", 100)),
                            value=default,
                            step=int(field.get("step", 1)),
                            help=help_,
                            key=f"{selected_disease}_{key}",
                        )

                    elif ftype == "select":
                        options  = field.get("options", {})
                        opt_keys = list(options.keys())
                        default_key = field.get("default", opt_keys[0])

                        # If PDF gave a numeric value, try to match it to an option
                        if pdf_val is not None:
                            for ok, ov in options.items():
                                if float(ov) == float(pdf_val):
                                    default_key = ok
                                    break

                        selected_key  = st.selectbox(
                            display_label,
                            options=opt_keys,
                            index=opt_keys.index(default_key) if default_key in opt_keys else 0,
                            help=help_,
                            key=f"{selected_disease}_{key}",
                        )
                        form_data[key] = options[selected_key]

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Predict button ─────────────────────────────────────────
        predict_col, _, _ = st.columns([1, 1, 1])
        with predict_col:
            submitted = st.form_submit_button(
                "🔮  Run Prediction",
                use_container_width=True,
                type="primary",
            )

    # ── Handle prediction ─────────────────────────────────────────
    if submitted:
        is_valid, errors = validate_patient_data(form_data, selected_disease)

        if not is_valid:
            for err in errors:
                st.error(f"❌ {err}")
        else:
            with st.spinner("Running AI inference…"):
                try:
                    result = predict_disease(form_data, selected_disease)
                    st.session_state[f"last_result_{selected_disease}"] = result
                    st.session_state[f"last_form_{selected_disease}"]   = form_data
                    st.session_state[f"patient_info_{selected_disease}"] = {
                        "name":      patient_name or "Anonymous",
                        "age":       patient_age_form,
                        "gender":    patient_gender_form,
                        "report_id": f"MP-{uuid.uuid4().hex[:8].upper()}",
                    }
                except Exception as e:
                    st.error(f"Prediction error: {e}")

    # ── Results panel ─────────────────────────────────────────────
    result_key = f"last_result_{selected_disease}"
    if result_key in st.session_state:
        _render_results(
            result       = st.session_state[result_key],
            form_data    = st.session_state.get(f"last_form_{selected_disease}", {}),
            patient_info = st.session_state.get(f"patient_info_{selected_disease}", {}),
            meta         = meta,
            disease      = selected_disease,
        )


# ═══════════════════════════════════════════════════════════════════
def _render_results(result: dict, form_data: dict, patient_info: dict,
                    meta: dict, disease: str):
    """Render the prediction results panel + download button."""

    st.markdown("---")
    st.markdown(
        "<h3 style='color:#E0E6F0;'>📊 Prediction Results</h3>",
        unsafe_allow_html=True,
    )

    is_positive   = result.get("prediction") == 1
    confidence    = result.get("confidence", 0.0)
    risk_level    = result.get("risk_level", "UNKNOWN")
    is_dummy      = result.get("is_dummy", False)

    # ── Colour scheme ──────────────────────────────────────────────
    if is_positive:
        result_color  = "#E63946"
        result_bg     = "#2A0A0A"
        result_border = "#E6394640"
        result_icon   = "🔴"
        result_text   = f"POSITIVE — {meta['label']} Likely Detected"
    else:
        result_color  = "#06D6A0"
        result_bg     = "#0A2A1A"
        result_border = "#06D6A040"
        result_icon   = "🟢"
        result_text   = f"NEGATIVE — No {meta['label']} Detected"

    risk_colors = {"HIGH": "#E63946", "MEDIUM": "#FFB703", "LOW": "#06D6A0"}
    risk_color  = risk_colors.get(risk_level, "#8899AA")

    # ── Main result card ──────────────────────────────────────────
    st.markdown(f"""
    <div style="
        background: {result_bg};
        border: 2px solid {result_color};
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1rem;
        text-align: center;
    ">
        <div style="font-size:3rem; margin-bottom:0.5rem;">{result_icon}</div>
        <div style="font-size:1.6rem; font-weight:800; color:{result_color};
                    margin-bottom:0.5rem;">{result_text}</div>
        <div style="color:#8899AA; font-size:0.88rem;">
            {meta['icon']} {meta['label']} &nbsp;·&nbsp;
            {datetime.now().strftime('%d %b %Y, %H:%M')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Metric row ────────────────────────────────────────────────
    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(f"""
        <div style="background:#0D1B2A;border:1px solid #1A3A5C;border-radius:12px;
                    padding:1rem;text-align:center;">
            <div style="font-size:2rem;font-weight:800;color:{result_color};">
                {confidence:.1f}%
            </div>
            <div style="color:#8899AA;font-size:0.82rem;margin-top:0.3rem;">
                Model Confidence
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div style="background:#0D1B2A;border:1px solid #1A3A5C;border-radius:12px;
                    padding:1rem;text-align:center;">
            <div style="font-size:2rem;font-weight:800;color:{risk_color};">
                {risk_level}
            </div>
            <div style="color:#8899AA;font-size:0.82rem;margin-top:0.3rem;">
                Risk Level
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        threshold = result.get("threshold_used", 0.45)
        st.markdown(f"""
        <div style="background:#0D1B2A;border:1px solid #1A3A5C;border-radius:12px;
                    padding:1rem;text-align:center;">
            <div style="font-size:2rem;font-weight:800;color:#00B4D8;">
                {threshold:.2f}
            </div>
            <div style="color:#8899AA;font-size:0.82rem;margin-top:0.3rem;">
                Decision Threshold
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Confidence bar ────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Confidence Gauge**")
    st.progress(int(confidence))
    st.caption(f"The model is {confidence:.1f}% confident in this prediction. "
               f"Threshold for positive: {threshold:.0%}")

    # ── AI Explanation ────────────────────────────────────────────
    importance = result.get("feature_importance", [])
    if importance:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**🔍 Top Contributing Factors (AI Explanation)**")
        st.caption(
            "Positive impact → pushed toward disease risk. "
            "Negative impact → pushed away from risk."
        )

        for row in importance[:6]:
            feat   = row["feature"]
            val    = row["value"]
            impact = row["impact"]
            bar    = abs(impact) * 200  # scale for visual bar
            color  = "#E63946" if impact > 0 else "#06D6A0"
            direction = "↑ Risk" if impact > 0 else "↓ Risk"

            st.markdown(f"""
            <div style="display:flex;align-items:center;margin:4px 0;gap:8px;">
                <div style="width:140px;font-size:0.82rem;color:#E0E6F0;
                            text-align:right;white-space:nowrap;overflow:hidden;
                            text-overflow:ellipsis;" title="{feat}">{feat}</div>
                <div style="flex:1;background:#1A2A3A;border-radius:4px;height:18px;
                            position:relative;overflow:hidden;">
                    <div style="width:{min(bar, 100):.0f}%;height:100%;
                                background:{color}40;border-radius:4px;
                                border-right:2px solid {color};"></div>
                </div>
                <div style="width:60px;font-size:0.78rem;color:{color};">{direction}</div>
                <div style="width:45px;font-size:0.78rem;color:#8899AA;">{impact:+.3f}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Input Summary ─────────────────────────────────────────────
    with st.expander("📋 View Entered Values"):
        cols_per_row = 3
        keys    = list(form_data.keys())
        for i in range(0, len(keys), cols_per_row):
            row_cols = st.columns(cols_per_row)
            for j, col in enumerate(row_cols):
                if i + j < len(keys):
                    k = keys[i + j]
                    v = form_data[k]
                    col.metric(k.replace("_", " ").title(), v)

    # ── Demo mode notice ──────────────────────────────────────────
    if is_dummy:
        st.warning(
            "🔧 **Demo Mode Active:** Model pkl files are not loaded. "
            "These results are generated by a placeholder and are not clinically valid. "
            "Add your trained `.pkl` files to `models/` to activate real predictions.",
        )

    # ── Download report ───────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**📄 Download Report**")

    dl_col1, dl_col2 = st.columns([1, 2])
    with dl_col1:
        try:
            pdf_bytes = generate_report_pdf(
                patient_info  = patient_info,
                result        = result,
                disease_label = meta["label"],
                patient_data  = form_data,
            )
            if pdf_bytes:
                report_id = patient_info.get("report_id", "report")
                st.download_button(
                    label     = "⬇️  Download PDF Report",
                    data      = pdf_bytes,
                    file_name = f"MediPredict_{meta['label']}_{report_id}.pdf",
                    mime      = "application/pdf",
                    type      = "primary",
                    use_container_width=True,
                )
            else:
                st.info("Install `fpdf2` to enable PDF report downloads.")
        except Exception as e:
            st.error(f"Report generation failed: {e}")

    with dl_col2:
        st.markdown("""
        <div style="background:#0D1B2A;border:1px solid #1A3A5C;border-radius:10px;
                    padding:0.8rem 1rem;font-size:0.82rem;color:#8899AA;">
            📋 The report includes: patient info, prediction result, confidence,
            all input values, top AI-explained factors, and a medical disclaimer.
        </div>
        """, unsafe_allow_html=True)

    # ── Medical disclaimer ────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(
        "⚕️ **This is a screening tool only.** Results are not a medical diagnosis. "
        "Please consult a qualified healthcare professional before taking any medical action.",
    )
