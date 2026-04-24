# app.py — MediPredict AI  ·  Main Entry Point
# ─────────────────────────────────────────────────────────────────
# Run locally:  streamlit run app.py
# Deploy:       Push to GitHub → deploy on share.streamlit.io
#               Make sure runtime.txt = python-3.11
# ─────────────────────────────────────────────────────────────────

import streamlit as st

# ── Page config (MUST be first Streamlit call) ─────────────────
st.set_page_config(
    page_title  = "MediPredict AI",
    page_icon   = "🧬",
    layout      = "wide",
    initial_sidebar_state = "expanded",
    menu_items  = {
        "Get Help":    "https://github.com/your-repo",
        "Report a bug": "https://github.com/your-repo/issues",
        "About":       "MediPredict AI — Multi-Disease Prediction System v1.0",
    },
)

# ── Load custom CSS ────────────────────────────────────────────
import os
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Import components ──────────────────────────────────────────
from components.sidebar      import render_sidebar
from components.home         import render_home
from components.diagnostics  import render_diagnostics
from components.about        import render_about

# ── Session state defaults ─────────────────────────────────────
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "home"

# ── Render sidebar (returns active tab) ────────────────────────
active_tab = render_sidebar()

# ── Route to correct tab ───────────────────────────────────────
if active_tab == "home":
    render_home()

elif active_tab == "diagnostics":
    render_diagnostics()

elif active_tab == "about":
    render_about()

else:
    render_home()
