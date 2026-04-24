# components/home.py
# ─────────────────────────────────────────────────────────────────
# Home / landing page:
#   • Hero banner
#   • Disease overview cards
#   • How it works
#   • Model accuracy badges
# ─────────────────────────────────────────────────────────────────

import streamlit as st
from utils.constants import DISEASE_META


def render_home():
    """Render the full Home tab."""

    # ── Hero ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0A0F1E 0%, #0D2137 60%, #091828 100%);
        border: 1px solid #1A3A5C;
        border-radius: 16px;
        padding: 3rem 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
    ">
        <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🧬</div>
        <h1 style="
            color: #00B4D8;
            font-size: 2.6rem;
            font-weight: 900;
            margin: 0 0 0.5rem 0;
            letter-spacing: -0.5px;
        ">MediPredict AI</h1>
        <p style="
            color: #90A8C0;
            font-size: 1.15rem;
            max-width: 650px;
            margin: 0 auto 1.5rem auto;
            line-height: 1.7;
        ">
            An AI-powered multi-disease screening system trained on clinical datasets.
            Get instant risk assessments for <strong style="color:#E0E6F0;">5 conditions</strong>
            — Diabetes, Kidney Disease, Liver Disease, Hypothyroid, and Anemia.
        </p>
        <div style="display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;">
            <span style="background:#0D3A4F;color:#00B4D8;padding:6px 16px;
                         border-radius:20px;font-size:0.85rem;border:1px solid #1A6A8F;">
                🤖 Ensemble ML Models
            </span>
            <span style="background:#0D3A4F;color:#00B4D8;padding:6px 16px;
                         border-radius:20px;font-size:0.85rem;border:1px solid #1A6A8F;">
                📄 PDF Lab Report Upload
            </span>
            <span style="background:#0D3A4F;color:#00B4D8;padding:6px 16px;
                         border-radius:20px;font-size:0.85rem;border:1px solid #1A6A8F;">
                📊 Downloadable Reports
            </span>
            <span style="background:#0D3A4F;color:#00B4D8;padding:6px 16px;
                         border-radius:20px;font-size:0.85rem;border:1px solid #1A6A8F;">
                🔍 AI Explainability
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick Start CTA ────────────────────────────────────────────
    col_l, col_c, col_r = st.columns([2, 1, 2])
    with col_c:
        if st.button("🔬  Start Diagnosis", use_container_width=True, type="primary"):
            st.session_state.active_tab = "diagnostics"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Disease Cards ──────────────────────────────────────────────
    st.markdown(
        "<h3 style='color:#E0E6F0;margin-bottom:1rem;'>🩺 Covered Conditions</h3>",
        unsafe_allow_html=True,
    )

    cols = st.columns(len(DISEASE_META))
    for col, (key, meta) in zip(cols, DISEASE_META.items()):
        with col:
            # Approximate accuracy values (replace with real test-set scores later)
            DUMMY_ACCURACY = {
                "diabetes":    {"acc": "91%", "recall": "88%", "auc": "0.94"},
                "kidney":      {"acc": "97%", "recall": "96%", "auc": "0.99"},
                "liver":       {"acc": "78%", "recall": "82%", "auc": "0.85"},
                "hypothyroid": {"acc": "95%", "recall": "93%", "auc": "0.97"},
                "anemia":      {"acc": "96%", "recall": "95%", "auc": "0.98"},
            }
            stats = DUMMY_ACCURACY[key]

            st.markdown(f"""
            <div style="
                background: #0D1B2A;
                border: 1px solid {meta['color']}40;
                border-top: 4px solid {meta['color']};
                border-radius: 12px;
                padding: 1.2rem;
                height: 220px;
                position: relative;
            ">
                <div style="font-size:2rem;">{meta['icon']}</div>
                <div style="font-weight:700;color:#E0E6F0;font-size:1rem;
                            margin:0.4rem 0 0.3rem 0;">
                    {meta['label']}
                </div>
                <div style="font-size:0.78rem;color:#8899AA;line-height:1.4;
                            margin-bottom:0.8rem;">
                    {meta['description']}
                </div>
                <div style="display:flex;gap:6px;flex-wrap:wrap;">
                    <span style="background:{meta['color']}20;color:{meta['color']};
                                 padding:2px 8px;border-radius:10px;font-size:0.72rem;">
                        Acc {stats['acc']}
                    </span>
                    <span style="background:{meta['color']}20;color:{meta['color']};
                                 padding:2px 8px;border-radius:10px;font-size:0.72rem;">
                        AUC {stats['auc']}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── How It Works ──────────────────────────────────────────────
    st.markdown(
        "<h3 style='color:#E0E6F0;margin-bottom:1.2rem;'>⚙️ How It Works</h3>",
        unsafe_allow_html=True,
    )

    steps = [
        ("1", "🎯", "Choose Disease", "Select from 5 conditions: Diabetes, Kidney, Liver, Thyroid, or Anemia."),
        ("2", "📋", "Enter Lab Values", "Fill the clinical form manually, or upload a lab report PDF for auto-extraction."),
        ("3", "🤖", "AI Prediction", "Our ensemble model (RF + XGBoost) runs the inference pipeline — impute → scale → predict."),
        ("4", "📄", "Download Report", "Get a detailed PDF report with the result, risk level, AI explanation, and a disclaimer."),
    ]

    step_cols = st.columns(4)
    for col, (num, icon, title, desc) in zip(step_cols, steps):
        with col:
            st.markdown(f"""
            <div style="
                background:#0D1B2A;
                border:1px solid #1A3A5C;
                border-radius:12px;
                padding:0.8rem;
                text-align:center;
                height:190px;
            ">
                <div style="
                    background:#00B4D820;
                    color:#00B4D8;
                    width:36px; height:36px;
                    border-radius:50%;
                    display:flex; align-items:center; justify-content:center;
                    font-weight:800; font-size:1rem;
                    margin:0 auto 0.6rem auto;
                    border:2px solid #00B4D860;
                ">{num}</div>
                <div style="font-size:1.6rem;margin-bottom:0.4rem;">{icon}</div>
                <div style="font-weight:700;color:#E0E6F0;font-size:0.9rem;
                            margin-bottom:0.4rem;">{title}</div>
                <div style="font-size:0.78rem;color:#8899AA;line-height:1.4;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tech Stack ────────────────────────────────────────────────
    st.markdown(
        "<h3 style='color:#E0E6F0;margin-bottom:1rem;'>🛠 Tech Stack</h3>",
        unsafe_allow_html=True,
    )

    tech_cols = st.columns(3)
    tech_items = [
        ("🤖 ML Models", [
            "scikit-learn 1.6.1 · Random Forest",
            "XGBoost 3.2.0 · Gradient Boosting",
            "LightGBM 4.6.0 (available)",
            "SMOTE for class imbalance",
        ]),
        ("🧪 Data Pipeline", [
            "SimpleImputer (median) — post-split",
            "StandardScaler for feature scaling",
            "Threshold tuning on validation set",
            "SHAP for explainability",
        ]),
        ("🖥 Deployment", [
            "Streamlit ≥ 1.39.0",
            "Python 3.11 · Streamlit Cloud",
            "fpdf2 for PDF report generation",
            "PyMuPDF for lab PDF extraction",
        ]),
    ]

    for col, (title, items) in zip(tech_cols, tech_items):
        with col:
            items_html = "".join(
                f"<li style='color:#8899AA;font-size:0.82rem;margin:3px 0;'>{i}</li>"
                for i in items
            )
            st.markdown(f"""
            <div style="background:#0D1B2A;border:1px solid #1A3A5C;
                        border-radius:12px;padding:1.2rem;">
                <div style="font-weight:700;color:#00B4D8;
                            margin-bottom:0.7rem;">{title}</div>
                <ul style="margin:0;padding-left:1.1rem;">{items_html}</ul>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Important Notice ──────────────────────────────────────────
    st.warning(
        "⚠️ **Medical Disclaimer:** MediPredict AI is a screening tool built for "
        "educational and demonstration purposes. It is **not** a substitute for "
        "professional medical advice, diagnosis, or treatment. Always consult a "
        "qualified healthcare provider.",
        icon=None,
    )
