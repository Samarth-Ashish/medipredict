# utils/predictor.py
# ─────────────────────────────────────────────────────────────────
# Prediction layer.
# ── NOW:  Returns structured dummy results so the UI is fully testable.
# ── LATER: Uncomment the real inference block below (load_model +
#            predict_disease) once your .pkl files are placed in models/
# ─────────────────────────────────────────────────────────────────
#
# HOW TO ACTIVATE REAL INFERENCE (3 steps):
#   1. Place your pkl files in  medipredict/models/
#      e.g.  models/diabetes_model.pkl,  models/diabetes_scaler.pkl, ...
#   2. Comment out the  DUMMY BLOCK  section.
#   3. Uncomment the   REAL INFERENCE BLOCK  section.
# ─────────────────────────────────────────────────────────────────

import os
import random

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")


# ─── Utility: check which models are on disk ──────────────────────
def get_loaded_models() -> list[str]:
    """Return list of disease names whose pkl artifacts are present."""
    loaded = []
    for disease in ["anemia", "diabetes", "hypothyroid", "kidney", "liver"]:
        model_path = os.path.join(MODELS_DIR, f"{disease}_model.pkl")
        if os.path.exists(model_path):
            loaded.append(disease)
    return loaded


# ═══════════════════════════════════════════════════════════════════
# DUMMY BLOCK  — delete / comment when real models are available
# ═══════════════════════════════════════════════════════════════════
def predict_disease(patient_data: dict, disease_name: str) -> dict:
    """
    DUMMY predictor — returns fake results for UI development.
    Replace with real inference once pkl files are present.
    """
    import random

    # Deterministic-ish seed so the same inputs always give the same fake output
    seed = int(sum(float(v) if isinstance(v, (int, float)) else 0
                   for v in patient_data.values())) % 100
    random.seed(seed)

    prob = random.uniform(0.15, 0.88)
    threshold = 0.45

    if prob >= 0.70:
        risk_level = "HIGH"
    elif prob >= 0.40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "disease":        disease_name,
        "prediction":     1 if prob >= threshold else 0,
        "label":          "POSITIVE (Disease Detected)" if prob >= threshold else "NEGATIVE (No Disease)",
        "confidence":     round(prob * 100, 2),
        "threshold_used": threshold,
        "risk_level":     risk_level,
        "is_dummy":       True,   # ← flag: remove once real models load
        "feature_importance": _dummy_feature_importance(patient_data),
    }


def _dummy_feature_importance(patient_data: dict) -> list[dict]:
    """Return fake SHAP-style feature importances for UI testing."""
    keys = list(patient_data.keys())
    random.shuffle(keys)
    result = []
    for k in keys[:6]:
        impact = round(random.uniform(-0.3, 0.4), 3)
        result.append({"feature": k, "value": patient_data[k], "impact": impact})
    return sorted(result, key=lambda x: abs(x["impact"]), reverse=True)


# ═══════════════════════════════════════════════════════════════════
# REAL INFERENCE BLOCK  — uncomment when pkl files are ready
# ═══════════════════════════════════════════════════════════════════
# import pickle
# import pandas as pd
#
# def predict_disease(patient_data: dict, disease_name: str) -> dict:
#     """
#     Real inference using trained pkl artifacts.
#     Pipeline: raw input → impute (median) → scale → predict.
#     """
#     def _load(name):
#         path = os.path.join(MODELS_DIR, f"{disease_name}_{name}.pkl")
#         with open(path, "rb") as f:
#             return pickle.load(f)
#
#     model         = _load("model")
#     scaler        = _load("scaler")
#     imputer       = _load("imputer")
#     feature_names = _load("feature_names")
#     threshold     = _load("threshold")
#
#     patient_df = pd.DataFrame([patient_data])[feature_names]
#
#     patient_imputed = pd.DataFrame(
#         imputer.transform(patient_df), columns=feature_names
#     )
#     patient_scaled = scaler.transform(patient_imputed)
#
#     probability = model.predict_proba(patient_scaled)[0, 1]
#     prediction  = 1 if probability >= threshold else 0
#
#     if probability >= 0.70:
#         risk_level = "HIGH"
#     elif probability >= 0.40:
#         risk_level = "MEDIUM"
#     else:
#         risk_level = "LOW"
#
#     return {
#         "disease":        disease_name,
#         "prediction":     prediction,
#         "label":          "POSITIVE (Disease Detected)" if prediction == 1 else "NEGATIVE (No Disease)",
#         "confidence":     round(probability * 100, 2),
#         "threshold_used": threshold,
#         "risk_level":     risk_level,
#         "is_dummy":       False,
#         "feature_importance": [],
#     }
