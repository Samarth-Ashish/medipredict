# utils/predictor.py

import os
import pickle
import pandas as pd

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")


def get_loaded_models() -> list[str]:
    loaded = []
    for disease in ["anemia", "diabetes", "hypothyroid", "kidney", "liver"]:
        if os.path.exists(os.path.join(MODELS_DIR, f"{disease}_model.pkl")):
            loaded.append(disease)
    return loaded


def predict_disease(patient_data: dict, disease_name: str) -> dict:
    def _load(name):
        with open(os.path.join(MODELS_DIR, f"{disease_name}_{name}.pkl"), "rb") as f:
            return pickle.load(f)

    model         = _load("model")
    scaler        = _load("scaler")
    imputer       = _load("imputer")
    feature_names = _load("feature_names")
    threshold     = _load("threshold")

    patient_df = pd.DataFrame([patient_data])[feature_names]

    patient_imputed = pd.DataFrame(
        imputer.transform(patient_df), columns=feature_names
    )
    patient_scaled = scaler.transform(patient_imputed)

    probability = model.predict_proba(patient_scaled)[0, 1]
    prediction  = 1 if probability >= threshold else 0

    risk_level = "HIGH" if probability >= 0.70 else "MEDIUM" if probability >= 0.40 else "LOW"

    # ── SHAP ──────────────────────────────────────────────────────
    feature_importance = []
    try:
        import shap

        # Works for standalone XGBoost (your case) AND VotingClassifier
        if hasattr(model, "estimators_"):
            xgb_model = dict(model.estimators_)["xgb"]
        else:
            xgb_model = model

        explainer   = shap.TreeExplainer(xgb_model)
        shap_values = explainer(patient_scaled)

        raw_shap = shap_values.values[0]  # 1-D array, one value per feature

        feature_importance = sorted(
            [
                {
                    "feature": feat,
                    "value":   round(float(patient_data.get(feat, 0)), 4),
                    "impact":  round(float(raw_shap[i]), 4),
                }
                for i, feat in enumerate(feature_names)
            ],
            key=lambda x: abs(x["impact"]),
            reverse=True,
        )
    except Exception:
        feature_importance = []
    # ─────────────────────────────────────────────────────────────

    return {
        "disease":            disease_name,
        "prediction":         prediction,
        "label":              "POSITIVE (Disease Detected)" if prediction == 1 else "NEGATIVE (No Disease)",
        "confidence":         round(probability * 100, 2),
        "threshold_used":     threshold,
        "risk_level":         risk_level,
        "is_dummy":           False,
        "feature_importance": feature_importance,
    }
