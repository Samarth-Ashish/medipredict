# components/sidebar.py
# ─────────────────────────────────────────────────────────────────
# Left sidebar: navigation + model status + disclaimer
# ─────────────────────────────────────────────────────────────────

import streamlit as st
from utils.predictor import get_loaded_models
from utils.constants import DISEASE_META


def render_sidebar() -> str:
    """
    Render the sidebar and return the currently active tab name.
    Returns one of: "home" | "diagnostics" | "about"
    """
    with st.sidebar:
        # ── Logo / Brand ──────────────────────────────────────────
        st.markdown("""
        <div style="text-align:center; padding: 1rem 0 0.5rem 0;">
            <div style="font-size:2.8rem;">🧬</div>
            <div style="font-size:1.4rem; font-weight:800;
                        color:#00B4D8; letter-spacing:1px;">
                MediPredict
            </div>
            <div style="font-size:0.75rem; color:#8899AA;
                        letter-spacing:2px; text-transform:uppercase;">
                AI Disease Screening
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ── Navigation ────────────────────────────────────────────
        st.markdown("**Navigation**")

        nav_options = {
            "🏠  Home":        "home",
            "🔬  Diagnostics": "diagnostics",
            "ℹ️  About / Help":  "about",
        }

        if "active_tab" not in st.session_state:
            st.session_state.active_tab = "home"

        for label, key in nav_options.items():
            is_active = st.session_state.active_tab == key
            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.active_tab = key
                st.rerun()

        st.divider()

        # ── Model Status ──────────────────────────────────────────
        st.markdown("**Model Status**")
        loaded = get_loaded_models()

        for disease, meta in DISEASE_META.items():
            is_loaded = disease in loaded
            icon   = "🟢" if is_loaded else "🔴"
            status = "Ready" if is_loaded else "No model"
            st.markdown(
                f"{icon} **{meta['icon']} {meta['label']}** — "
                f"<span style='color:{'#4CAF50' if is_loaded else '#FF6B6B'};"
                f"font-size:0.8rem'>{status}</span>",
                unsafe_allow_html=True,
            )

        if not loaded:
            st.info(
                "📂 Place your `.pkl` files in the `models/` folder to "
                "activate real predictions.",
                icon="ℹ️",
            )

        st.divider()

        # ── Disclaimer ────────────────────────────────────────────
        st.markdown("""
        <div style="font-size:0.72rem; color:#8899AA; line-height:1.5;">
            ⚠️ <b>Medical Disclaimer</b><br>
            This tool is for educational/screening
            purposes only and does <b>not</b> replace
            professional medical diagnosis. Always
            consult a licensed physician.
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            "<div style='font-size:0.65rem;color:#556;margin-top:1rem;'>"
            "v1.0 · Built with Streamlit · Models: sklearn 1.6.1</div>",
            unsafe_allow_html=True,
        )

    return st.session_state.active_tab
