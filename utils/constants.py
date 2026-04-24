# utils/constants.py
# ─────────────────────────────────────────────────────────────────
# Central config for all 5 diseases:
#   • Feature names & order (must match training)
#   • UI labels, help text, input types, ranges
#   • Disease metadata (icon, colour, description)
# ─────────────────────────────────────────────────────────────────

DISEASE_META = {
    "diabetes": {
        "label":       "Diabetes",
        "icon":        "🩸",
        "color":       "#E63946",
        "description": "Predicts likelihood of Type-2 Diabetes using the Pima Indians dataset (NIDDK).",
        "model_type":  "xgboost",
        "target_label": "Diabetic",
    },
    "kidney": {
        "label":       "Kidney Disease",
        "icon":        "🫘",
        "color":       "#F4A261",
        "description": "Detects Chronic Kidney Disease (CKD) from blood/urine laboratory markers.",
        "model_type":  "xgboost",
        "target_label": "CKD Positive",
    },
    "liver": {
        "label":       "Liver Disease",
        "icon":        "🟤",
        "color":       "#E9C46A",
        "description": "Identifies Liver Disease risk using Indian Liver Patient Dataset (ILPD).",
        "model_type":  "xgboost",
        "target_label": "Liver Disease",
    },
    "hypothyroid": {
        "label":       "Hypothyroid",
        "icon":        "🦋",
        "color":       "#2A9D8F",
        "description": "Screens for Hypothyroidism using thyroid function panel values.",
        "model_type":  "xgboost",
        "target_label": "Hypothyroid",
    },
    "anemia": {
        "label":       "Anemia",
        "icon":        "💉",
        "color":       "#A8DADC",
        "description": "Detects Anemia from complete blood count (CBC) markers.",
        "model_type":  "xgboost",
        "target_label": "Anemic",
    },
}

# ─────────────────────────────────────────────────────────────────
# FIELD SPEC SCHEMA:
#   type        → "number" | "select" | "slider"
#   label       → UI display label
#   help        → tooltip / explanation
#   min/max/step→ for number/slider
#   default     → pre-filled value
#   options     → for select fields  {display: internal_value}
#   unit        → display unit string
# ─────────────────────────────────────────────────────────────────

DISEASE_FEATURES = {

    # ── DIABETES ──────────────────────────────────────────────────
    "diabetes": [
        {
            "key": "Pregnancies", "type": "number",
            "label": "Number of Pregnancies", "unit": "",
            "min": 0, "max": 20, "step": 1, "default": 1,
            "help": "Total number of times pregnant. Enter 0 for males.",
        },
        {
            "key": "Glucose", "type": "slider",
            "label": "Plasma Glucose (2hr OGTT)", "unit": "mg/dL",
            "min": 50, "max": 250, "step": 1, "default": 110,
            "help": "Plasma glucose concentration after 2-hour oral glucose tolerance test.",
        },
        {
            "key": "BloodPressure", "type": "slider",
            "label": "Diastolic Blood Pressure", "unit": "mm Hg",
            "min": 20, "max": 140, "step": 1, "default": 72,
            "help": "Diastolic blood pressure reading.",
        },
        {
            "key": "SkinThickness", "type": "slider",
            "label": "Skin Fold Thickness (Triceps)", "unit": "mm",
            "min": 0, "max": 100, "step": 1, "default": 23,
            "help": "Triceps skin fold thickness. Leave at 0 if unknown (will be imputed).",
        },
        {
            "key": "Insulin", "type": "slider",
            "label": "2-Hour Serum Insulin", "unit": "µU/mL",
            "min": 0, "max": 900, "step": 1, "default": 0,
            "help": "2-hour serum insulin level. Leave at 0 if unknown (will be imputed by model).",
        },
        {
            "key": "BMI", "type": "slider",
            "label": "Body Mass Index (BMI)", "unit": "kg/m²",
            "min": 10.0, "max": 70.0, "step": 0.1, "default": 28.0,
            "help": "Weight in kg / (Height in m)². Normal range: 18.5–24.9.",
        },
        {
            "key": "DiabetesPedigreeFunction", "type": "number",
            "label": "Diabetes Pedigree Function", "unit": "",
            "min": 0.0, "max": 3.0, "step": 0.001, "default": 0.471,
            "help": "Family history score: higher = stronger family history of diabetes.",
        },
        {
            "key": "Age", "type": "slider",
            "label": "Age", "unit": "years",
            "min": 1, "max": 120, "step": 1, "default": 33,
            "help": "Patient age in years.",
        },
    ],

    # ── KIDNEY DISEASE ─────────────────────────────────────────────
    "kidney": [
        {
            "key": "age",  "type": "slider", "label": "Age", "unit": "years",
            "min": 1, "max": 100, "step": 1, "default": 45,
            "help": "Patient age in years.",
        },
        {
            "key": "bp", "type": "slider", "label": "Blood Pressure", "unit": "mm Hg",
            "min": 40, "max": 200, "step": 1, "default": 80,
            "help": "Diastolic blood pressure.",
        },
        {
            "key": "sg", "type": "select", "label": "Specific Gravity", "unit": "",
            "options": {"1.005": 1.005, "1.010": 1.010, "1.015": 1.015,
                        "1.020": 1.020, "1.025": 1.025},
            "default": "1.015",
            "help": "Urine specific gravity — indicates kidney concentration ability.",
        },
        {
            "key": "al", "type": "select", "label": "Albumin in Urine", "unit": "",
            "options": {"0 (None)": 0, "1 (Trace)": 1, "2 (+)": 2,
                        "3 (++)": 3, "4 (+++)": 4, "5 (++++)": 5},
            "default": "0 (None)",
            "help": "Albumin present in urine (proteinuria). 0 = none, 5 = severe.",
        },
        {
            "key": "su", "type": "select", "label": "Sugar in Urine", "unit": "",
            "options": {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5},
            "default": "0",
            "help": "Sugar present in urine. 0 = none.",
        },
        {
            "key": "rbc", "type": "select", "label": "Red Blood Cells (urine)", "unit": "",
            "options": {"Normal": 0, "Abnormal": 1},
            "default": "Normal",
            "help": "RBC appearance in urine microscopy.",
        },
        {
            "key": "pc", "type": "select", "label": "Pus Cell (urine)", "unit": "",
            "options": {"Normal": 0, "Abnormal": 1},
            "default": "Normal",
            "help": "Pus cells in urine — indicator of infection.",
        },
        {
            "key": "pcc", "type": "select", "label": "Pus Cell Clumps", "unit": "",
            "options": {"Not Present": 0, "Present": 1},
            "default": "Not Present",
            "help": "Pus cell clumps in urine.",
        },
        {
            "key": "ba", "type": "select", "label": "Bacteria (urine)", "unit": "",
            "options": {"Not Present": 0, "Present": 1},
            "default": "Not Present",
            "help": "Presence of bacteria in urine.",
        },
        {
            "key": "bgr", "type": "slider", "label": "Blood Glucose Random", "unit": "mg/dL",
            "min": 50, "max": 500, "step": 1, "default": 120,
            "help": "Random blood glucose level.",
        },
        {
            "key": "bu", "type": "slider", "label": "Blood Urea", "unit": "mg/dL",
            "min": 5, "max": 200, "step": 1, "default": 30,
            "help": "Blood urea nitrogen — measures kidney waste filtration.",
        },
        {
            "key": "sc", "type": "number", "label": "Serum Creatinine", "unit": "mg/dL",
            "min": 0.1, "max": 20.0, "step": 0.1, "default": 1.0,
            "help": "Serum creatinine — key kidney function marker. Normal: ~0.6–1.2 mg/dL.",
        },
        {
            "key": "sod", "type": "slider", "label": "Sodium", "unit": "mEq/L",
            "min": 100, "max": 165, "step": 1, "default": 137,
            "help": "Serum sodium level. Normal: 135–145 mEq/L.",
        },
        {
            "key": "pot", "type": "number", "label": "Potassium", "unit": "mEq/L",
            "min": 1.0, "max": 10.0, "step": 0.1, "default": 4.5,
            "help": "Serum potassium level. Normal: 3.5–5.0 mEq/L.",
        },
        {
            "key": "hemo", "type": "number", "label": "Haemoglobin", "unit": "g/dL",
            "min": 3.0, "max": 20.0, "step": 0.1, "default": 13.5,
            "help": "Haemoglobin level. Normal: 12–17 g/dL.",
        },
        {
            "key": "pcv", "type": "slider", "label": "Packed Cell Volume (PCV)", "unit": "%",
            "min": 10, "max": 60, "step": 1, "default": 40,
            "help": "Hematocrit / PCV. Normal: 36–52%.",
        },
        {
            "key": "wc", "type": "slider", "label": "White Blood Cell Count", "unit": "cells/µL",
            "min": 2000, "max": 20000, "step": 100, "default": 7500,
            "help": "WBC count. Normal: 4,000–11,000 cells/µL.",
        },
        {
            "key": "rc", "type": "number", "label": "Red Blood Cell Count", "unit": "millions/µL",
            "min": 1.0, "max": 9.0, "step": 0.1, "default": 4.8,
            "help": "RBC count. Normal: 4.0–5.5 millions/µL.",
        },
        {
            "key": "htn", "type": "select", "label": "Hypertension", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Does the patient have hypertension?",
        },
        {
            "key": "dm", "type": "select", "label": "Diabetes Mellitus", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Does the patient have diabetes mellitus?",
        },
        {
            "key": "cad", "type": "select", "label": "Coronary Artery Disease", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Does the patient have coronary artery disease?",
        },
        {
            "key": "appet", "type": "select", "label": "Appetite", "unit": "",
            "options": {"Good": 1, "Poor": 0},
            "default": "Good",
            "help": "Patient's appetite status.",
        },
        {
            "key": "pe", "type": "select", "label": "Pedal Edema", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Swelling in feet/ankles due to fluid retention.",
        },
        {
            "key": "ane", "type": "select", "label": "Anemia", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Is anemia present?",
        },
    ],

    # ── LIVER DISEASE ──────────────────────────────────────────────
    "liver": [
        {
            "key": "age", "type": "slider", "label": "Age", "unit": "years",
            "min": 4, "max": 90, "step": 1, "default": 40,
            "help": "Patient age in years.",
        },
        {
            "key": "gender", "type": "select", "label": "Gender", "unit": "",
            "options": {"Male": 1, "Female": 0},
            "default": "Male",
            "help": "Patient gender.",
        },
        {
            "key": "total_bilirubin", "type": "number", "label": "Total Bilirubin", "unit": "mg/dL",
            "min": 0.1, "max": 75.0, "step": 0.1, "default": 1.0,
            "help": "Total bilirubin. Normal: 0.2–1.2 mg/dL. High = liver/bile duct issue.",
        },
        {
            "key": "direct_bilirubin", "type": "number", "label": "Direct Bilirubin", "unit": "mg/dL",
            "min": 0.0, "max": 30.0, "step": 0.1, "default": 0.3,
            "help": "Direct (conjugated) bilirubin. Normal: <0.3 mg/dL.",
        },
        {
            "key": "alkphos", "type": "slider", "label": "Alkaline Phosphatase (ALP)", "unit": "IU/L",
            "min": 60, "max": 2500, "step": 10, "default": 200,
            "help": "ALP enzyme level. Normal: 44–147 IU/L. Elevated = liver/bone disease.",
        },
        {
            "key": "sgpt", "type": "slider", "label": "SGPT / ALT", "unit": "IU/L",
            "min": 7, "max": 2000, "step": 5, "default": 35,
            "help": "Alanine Aminotransferase (ALT/SGPT). Normal: 7–56 IU/L.",
        },
        {
            "key": "sgot", "type": "slider", "label": "SGOT / AST", "unit": "IU/L",
            "min": 10, "max": 5000, "step": 5, "default": 30,
            "help": "Aspartate Aminotransferase (AST/SGOT). Normal: 10–40 IU/L.",
        },
        {
            "key": "total_proteins", "type": "number", "label": "Total Proteins", "unit": "g/dL",
            "min": 2.0, "max": 10.0, "step": 0.1, "default": 6.8,
            "help": "Total serum proteins. Normal: 6.0–8.3 g/dL.",
        },
        {
            "key": "albumin", "type": "number", "label": "Albumin", "unit": "g/dL",
            "min": 0.5, "max": 6.0, "step": 0.1, "default": 3.5,
            "help": "Serum albumin. Normal: 3.5–5.0 g/dL. Low = liver disease.",
        },
        {
            "key": "ag_ratio", "type": "number", "label": "A/G Ratio", "unit": "",
            "min": 0.1, "max": 3.0, "step": 0.01, "default": 1.05,
            "help": "Albumin to Globulin ratio. Normal: 1.0–2.5.",
        },
    ],

    # ── HYPOTHYROID ────────────────────────────────────────────────
    "hypothyroid": [
        {
            "key": "age", "type": "slider", "label": "Age", "unit": "years",
            "min": 1, "max": 100, "step": 1, "default": 40,
            "help": "Patient age.",
        },
        {
            "key": "sex", "type": "select", "label": "Sex", "unit": "",
            "options": {"Female": 0, "Male": 1},
            "default": "Female",
            "help": "Biological sex. Hypothyroidism is more common in females.",
        },
        {
            "key": "on thyroxine", "type": "select", "label": "On Thyroxine", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Is the patient currently taking thyroxine (T4) medication?",
        },
        {
            "key": "query on thyroxine", "type": "select", "label": "Query on Thyroxine", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Clinical query for thyroxine treatment.",
        },
        {
            "key": "on antithyroid medication", "type": "select",
            "label": "On Antithyroid Medication", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Is the patient on antithyroid medication?",
        },
        {
            "key": "sick", "type": "select", "label": "Currently Sick", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Is the patient currently sick with another illness?",
        },
        {
            "key": "pregnant", "type": "select", "label": "Pregnant", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Is the patient currently pregnant?",
        },
        {
            "key": "thyroid surgery", "type": "select", "label": "Thyroid Surgery History", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Has the patient had thyroid surgery?",
        },
        {
            "key": "I131 treatment", "type": "select", "label": "I131 Treatment", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Has the patient received radioactive iodine (I-131) treatment?",
        },
        {
            "key": "query hypothyroid", "type": "select", "label": "Query Hypothyroid", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Clinical suspicion for hypothyroidism.",
        },
        {
            "key": "query hyperthyroid", "type": "select", "label": "Query Hyperthyroid", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Clinical suspicion for hyperthyroidism.",
        },
        {
            "key": "lithium", "type": "select", "label": "On Lithium", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Is the patient on lithium? (Lithium affects thyroid function.)",
        },
        {
            "key": "goitre", "type": "select", "label": "Goitre Present", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Is goitre (thyroid swelling) present?",
        },
        {
            "key": "tumor", "type": "select", "label": "Tumor Present", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Is there a known tumor?",
        },
        {
            "key": "hypopituitary", "type": "select", "label": "Hypopituitarism", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Is hypopituitarism present?",
        },
        {
            "key": "psych", "type": "select", "label": "Psychiatric Condition", "unit": "",
            "options": {"No": 0, "Yes": 1},
            "default": "No",
            "help": "Is there a psychiatric condition present?",
        },
        {
            "key": "TSH", "type": "number", "label": "TSH Level", "unit": "mIU/L",
            "min": 0.0, "max": 100.0, "step": 0.01, "default": 2.5,
            "help": "Thyroid Stimulating Hormone. Normal: 0.4–4.0 mIU/L. High = Hypothyroid.",
        },
        {
            "key": "T3", "type": "number", "label": "T3 Level", "unit": "ng/dL",
            "min": 0.0, "max": 12.0, "step": 0.01, "default": 2.0,
            "help": "Triiodothyronine (T3). Normal: 0.8–2.0 ng/dL.",
        },
        {
            "key": "TT4", "type": "slider", "label": "Total T4 (TT4)", "unit": "µg/dL",
            "min": 0, "max": 300, "step": 1, "default": 90,
            "help": "Total Thyroxine. Normal: 60–120 µg/dL.",
        },
        {
            "key": "T4U", "type": "number", "label": "T4U (T4 Uptake)", "unit": "",
            "min": 0.1, "max": 3.0, "step": 0.01, "default": 1.0,
            "help": "T4 uptake (T-uptake). Reflects thyroid binding globulin capacity.",
        },
        {
            "key": "FTI", "type": "slider", "label": "Free Thyroxine Index (FTI)", "unit": "",
            "min": 0, "max": 400, "step": 1, "default": 90,
            "help": "Free Thyroxine Index = TT4 × T4U. Normal: 64–154.",
        },
    ],

    # ── ANEMIA ────────────────────────────────────────────────────
    "anemia": [
        {
            "key": "Gender", "type": "select", "label": "Gender", "unit": "",
            "options": {"Female": 0, "Male": 1},
            "default": "Female",
            "help": "Patient gender. Anemia is more common in females.",
        },
        {
            "key": "Hemoglobin", "type": "number", "label": "Haemoglobin (Hgb)", "unit": "g/dL",
            "min": 2.0, "max": 20.0, "step": 0.1, "default": 12.0,
            "help": "Haemoglobin concentration. Normal: Female 12–15.5 g/dL | Male 13.5–17.5 g/dL.",
        },
        {
            "key": "MCH", "type": "number", "label": "MCH", "unit": "pg",
            "min": 10.0, "max": 50.0, "step": 0.1, "default": 27.0,
            "help": "Mean Corpuscular Haemoglobin. Normal: 27–33 pg.",
        },
        {
            "key": "MCHC", "type": "number", "label": "MCHC", "unit": "g/dL",
            "min": 20.0, "max": 40.0, "step": 0.1, "default": 32.0,
            "help": "Mean Corpuscular Haemoglobin Concentration. Normal: 31.5–35 g/dL.",
        },
        {
            "key": "MCV", "type": "number", "label": "MCV", "unit": "fL",
            "min": 50.0, "max": 130.0, "step": 0.1, "default": 82.0,
            "help": "Mean Corpuscular Volume. Normal: 80–100 fL. Low = microcytic, High = macrocytic.",
        },
    ],
}

# ─── Dummy reference ranges shown in UI (for user guidance) ────────
REFERENCE_RANGES = {
    "Glucose":             {"normal": "70–99", "unit": "mg/dL", "note": "Fasting"},
    "BloodPressure":       {"normal": "60–80", "unit": "mm Hg", "note": "Diastolic"},
    "BMI":                 {"normal": "18.5–24.9", "unit": "kg/m²", "note": ""},
    "Hemoglobin":          {"normal": "12–17.5", "unit": "g/dL", "note": "Varies by sex"},
    "TSH":                 {"normal": "0.4–4.0", "unit": "mIU/L", "note": ""},
    "total_bilirubin":     {"normal": "0.2–1.2", "unit": "mg/dL", "note": ""},
    "sc":                  {"normal": "0.6–1.2", "unit": "mg/dL", "note": "Serum creatinine"},
}
