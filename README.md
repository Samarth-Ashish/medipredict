# 🧬 MediPredict AI — Multi-Disease Prediction System

An AI-powered disease screening web app built with Streamlit. Predicts risk for **5 conditions**:
Diabetes · Kidney Disease · Liver Disease · Hypothyroid · Anemia

---

## 📁 Folder Structure

```
medipredict/
│
├── app.py                        ← Main entry point (streamlit run app.py)
├── requirements.txt              ← Pinned dependencies (critical for pkl compatibility)
├── runtime.txt                   ← Python 3.11 (for Streamlit Cloud)
│
├── .streamlit/
│   └── config.toml               ← Dark theme + server config
│
├── models/                       ← 📂 Put your .pkl files here
│   ├── anemia_model.pkl
│   ├── anemia_scaler.pkl
│   ├── anemia_imputer.pkl
│   ├── anemia_feature_names.pkl
│   ├── anemia_threshold.pkl
│   ├── diabetes_model.pkl        ← (same 5 artifacts per disease)
│   ├── hypothyroid_model.pkl
│   ├── kidney_model.pkl
│   └── liver_model.pkl
│
├── components/                   ← UI building blocks (one file per section)
│   ├── __init__.py
│   ├── sidebar.py                ← Left sidebar, nav, model status
│   ├── home.py                   ← Home / landing page
│   ├── diagnostics.py            ← Main prediction form + results
│   ├── about.py                  ← About / help / FAQ
│   ├── report.py                 ← PDF report generator (fpdf2)
│   └── pdf_extractor.py          ← Lab PDF → field extractor (PyMuPDF)
│
├── utils/
│   ├── __init__.py
│   ├── constants.py              ← ALL disease feature configs & metadata
│   ├── predictor.py              ← Inference wrapper (dummy now → real later)
│   └── validators.py             ← Input validation
│
└── assets/
    └── style.css                 ← Global dark-theme CSS
```

---

## 🚀 Quick Start

### Local
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Streamlit Cloud
1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io) → New App
3. Set **Main file path** = `app.py`
4. Click Deploy — done!

---

## 🔧 Activating Real Predictions

1. Place your `.pkl` files in `models/`:
   ```
   {disease}_model.pkl
   {disease}_scaler.pkl
   {disease}_imputer.pkl
   {disease}_feature_names.pkl
   {disease}_threshold.pkl
   ```
   for each of: `anemia`, `diabetes`, `hypothyroid`, `kidney`, `liver`

2. In `utils/predictor.py`:
   - Comment out the **DUMMY BLOCK**
   - Uncomment the **REAL INFERENCE BLOCK**

---

## 🔒 Version Pinning (Critical!)

The `SimpleImputer` error occurs when sklearn versions mismatch between training and inference.
All versions in `requirements.txt` are pinned to match Google Colab's training environment:

```
scikit-learn==1.6.1   ← Must match Colab exactly
xgboost==3.2.0
lightgbm==4.6.0
imbalanced-learn==0.14.1
numpy==2.0.2
pandas==2.2.2
```

---

## ✏️ Adding a New Disease

1. Add to `DISEASE_META` in `utils/constants.py`
2. Add feature list to `DISEASE_FEATURES` in `utils/constants.py`
3. Train model in Colab, save pkl files, drop them in `models/`
4. That's it — the form builder in `diagnostics.py` is fully dynamic

---

## ⚠️ Disclaimer

This tool is for **educational and screening purposes only**.
It does not constitute a medical diagnosis. Always consult a licensed physician.
