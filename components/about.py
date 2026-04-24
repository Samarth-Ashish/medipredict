# components/about.py
# ─────────────────────────────────────────────────────────────────
# About / Help tab — project info, dataset info, FAQ, deployment guide
# ─────────────────────────────────────────────────────────────────

import streamlit as st


def render_about():
    """Render the About / Help tab."""

    st.markdown(
        "<h2 style='color:#00B4D8;'>ℹ️ About MediPredict AI</h2>",
        unsafe_allow_html=True,
    )

    # ── Project Summary ────────────────────────────────────────────
    with st.expander("📌 Project Overview", expanded=True):
        st.markdown("""
        **MediPredict AI** is a multi-disease prediction system trained using standard
        clinical datasets. The pipeline was developed in Google Colab and is deployed
        on Streamlit Cloud.

        **Goal:** Provide a fast, accessible screening interface for 5 common conditions
        using patient lab report values — without requiring any ML expertise from the user.

        **Architecture:**
        - Each disease has its own independently trained model
        - All models use the same training pipeline (train → impute → scale → SMOTE → fit → threshold-tune)
        - Artifacts saved as `.pkl` files: `model`, `scaler`, `imputer`, `feature_names`, `threshold`
        """)

    # ── Datasets ──────────────────────────────────────────────────
    with st.expander("📊 Datasets Used"):
        datasets = [
            ("🩸 Anemia",         "CBC dataset",                     "~1,400 rows", "5",  "Result (0/1)"),
            ("🩸 Diabetes",        "Pima Indians Diabetes (NIDDK)",    "768 rows",    "8",  "Outcome (0/1)"),
            ("🦋 Hypothyroid",     "UCI Hypothyroid Dataset",          "~3,772 rows", "21", "binaryClass (P/N)"),
            ("🫘 Kidney Disease",  "UCI CKD Dataset",                  "400 rows",    "24", "classification (ckd/notckd)"),
            ("🟤 Liver Disease",   "ILPD (Indian Liver Patient Data)", "~583 rows",   "10", "result (1/2)"),
        ]
        st.table({
            "Disease":  [d[0] for d in datasets],
            "Dataset":  [d[1] for d in datasets],
            "Rows":     [d[2] for d in datasets],
            "Features": [d[3] for d in datasets],
            "Target":   [d[4] for d in datasets],
        })

    # ── Training Pipeline ──────────────────────────────────────────
    with st.expander("⚙️ Training Pipeline"):
        st.markdown("""
        Each disease model follows this fixed pipeline in `train_disease_model()`:

        | Step | Action | Why |
        |------|--------|-----|
        | 1 | **60/20/20 split** (stratified) | Preserve class ratios |
        | 2 | **SimpleImputer** (median) — fit on train only | Prevent data leakage |
        | 3 | **StandardScaler** — fit on train only | Normalize feature magnitudes |
        | 4 | **SMOTE** — only on training fold | Balance imbalanced classes |
        | 5 | **VotingClassifier** (RF + XGBoost, soft) | Best of both worlds |
        | 6 | **Threshold tuning** on validation set | Maximize F1 / Recall |
        | 7 | **Evaluate** on held-out test set | Unbiased final metrics |

        > The `SimpleImputer` is saved to disk and applied identically at inference,
        > ensuring no training-inference mismatch.
        """)

    # ── Version Pinning ────────────────────────────────────────────
    with st.expander("🔒 Dependency Version Pinning (Why it matters)"):
        st.markdown("""
        The `SimpleImputer` error — **`'SimpleImputer' object has no attribute '_fill_dtype'`**
        — occurs because the pkl file was saved with one version of scikit-learn and loaded
        with a different version.

        **Fix:** Pin ALL libraries in `requirements.txt` to the **exact same versions**
        that were active in Google Colab when the models were trained:

        ```
        scikit-learn==1.6.1
        xgboost==3.2.0
        lightgbm==4.6.0
        imbalanced-learn==0.14.1
        numpy==2.0.2
        pandas==2.2.2
        ```

        And set `runtime.txt` to `python-3.11` to match the Colab Python version.
        """)

    # ── Deployment Guide ───────────────────────────────────────────
    with st.expander("🚀 Streamlit Cloud Deployment Guide"):
        st.markdown("""
        **Step-by-step to deploy:**

        1. **Clone / push this folder** to a GitHub repository (public or private).

        2. **Add your `.pkl` files** to the `models/` folder:
           ```
           models/
             anemia_model.pkl        anemia_scaler.pkl
             anemia_imputer.pkl      anemia_feature_names.pkl
             anemia_threshold.pkl
             diabetes_model.pkl      ...  (same pattern)
             hypothyroid_model.pkl   ...
             kidney_model.pkl        ...
             liver_model.pkl         ...
           ```

        3. **Go to** [share.streamlit.io](https://share.streamlit.io) → *New app*

        4. Select your GitHub repo, branch, and set **Main file path** to `app.py`

        5. Streamlit Cloud will install `requirements.txt` automatically.
           `runtime.txt` (`python-3.11`) pins the Python version.

        6. Click **Deploy** — first cold start may take 3–5 minutes.

        **Troubleshooting common errors:**

        | Error | Cause | Fix |
        |-------|-------|-----|
        | `_fill_dtype` attribute error | scikit-learn version mismatch | Pin `scikit-learn==1.6.1` in requirements.txt |
        | `numpy` dtype errors | numpy version mismatch | Pin `numpy==2.0.2` |
        | `ModuleNotFoundError: fitz` | PyMuPDF not installed | Add `PyMuPDF==1.24.14` to requirements.txt |
        | Memory limit exceeded | Large model pkl files | Use XGBoost-only models instead of ensemble |
        """)

    # ── FAQ ───────────────────────────────────────────────────────
    with st.expander("❓ Frequently Asked Questions"):
        faqs = [
            ("Is this a real diagnosis?",
             "No. This is a screening tool for educational purposes. Always consult a doctor."),
            ("Where do I get the .pkl model files?",
             "Train them in Google Colab using the provided training notebook, then download the zip."),
            ("Why do some fields show 0?",
             "0 values for fields like Insulin/SkinThickness are treated as missing and imputed by the model automatically."),
            ("Can I add a new disease?",
             "Yes. Add feature config to `utils/constants.py` under DISEASE_FEATURES and DISEASE_META, "
             "then add a new section in `components/diagnostics.py`'s form builder."),
            ("What is SHAP?",
             "SHAP (SHapley Additive exPlanations) explains which features pushed the model toward or away from a positive prediction."),
        ]
        for q, a in faqs:
            st.markdown(f"**Q: {q}**")
            st.markdown(f"A: {a}")
            st.markdown("---")
