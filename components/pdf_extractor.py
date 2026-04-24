# components/pdf_extractor.py
# ─────────────────────────────────────────────────────────────────
# Extracts numeric lab values from patient PDF reports.
# Uses PyMuPDF (fitz) for text extraction + regex patterns.
# ─────────────────────────────────────────────────────────────────
#
# PLACEHOLDER / REAL IMPLEMENTATION:
#   The patterns dict below maps feature keys → regex patterns.
#   Extend the patterns for your specific lab report format.
#
#   For now, extraction may return partial results; the form
#   pre-fills found values and leaves the rest for manual entry.
# ─────────────────────────────────────────────────────────────────

import re
import io

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False


# ── Regex patterns for common lab report fields ───────────────────
# Format: "feature_key": [list of regex patterns to try]
# Each pattern must have ONE named capture group called `val`

FIELD_PATTERNS = {
    # Diabetes
    "Glucose":                   [r"[Gg]lucose[\s:]+(?P<val>[\d.]+)"],
    "BloodPressure":             [r"[Dd]iastolic[\s:]+(?P<val>[\d.]+)",
                                   r"BP[\s/]*(?:\d+)/(?P<val>\d+)"],
    "SkinThickness":             [r"[Ss]kin\s*[Tt]hickness[\s:]+(?P<val>[\d.]+)"],
    "Insulin":                   [r"[Ii]nsulin[\s:]+(?P<val>[\d.]+)"],
    "BMI":                       [r"BMI[\s:]+(?P<val>[\d.]+)",
                                   r"[Bb]ody\s*[Mm]ass\s*[Ii]ndex[\s:]+(?P<val>[\d.]+)"],
    "Pregnancies":               [r"[Pp]regnancies?[\s:]+(?P<val>\d+)"],
    "Age":                       [r"[Aa]ge[\s:]+(?P<val>\d+)"],

    # Kidney
    "sc":                        [r"[Cc]reatinine[\s:]+(?P<val>[\d.]+)"],
    "bu":                        [r"(?:[Bb]lood\s*)?[Uu]rea[\s:]+(?P<val>[\d.]+)"],
    "hemo":                      [r"[Hh]a?emoglobin[\s:]+(?P<val>[\d.]+)"],
    "bp":                        [r"[Bb]lood\s*[Pp]ressure[\s:]+(?P<val>[\d.]+)"],
    "bgr":                       [r"[Bb]lood\s*[Gg]lucose\s*[Rr]andom[\s:]+(?P<val>[\d.]+)"],
    "sod":                       [r"[Ss]odium[\s:]+(?P<val>[\d.]+)"],
    "pot":                       [r"[Pp]otassium[\s:]+(?P<val>[\d.]+)"],

    # Liver
    "total_bilirubin":           [r"[Tt]otal\s*[Bb]ilirubin[\s:]+(?P<val>[\d.]+)"],
    "direct_bilirubin":          [r"[Dd]irect\s*[Bb]ilirubin[\s:]+(?P<val>[\d.]+)"],
    "alkphos":                   [r"(?:ALP|[Aa]lkaline\s*[Pp]hosphatase)[\s:]+(?P<val>[\d.]+)"],
    "sgpt":                      [r"(?:SGPT|ALT|[Aa]lanine)[\s:]+(?P<val>[\d.]+)"],
    "sgot":                      [r"(?:SGOT|AST|[Aa]spartate)[\s:]+(?P<val>[\d.]+)"],
    "total_proteins":            [r"[Tt]otal\s*[Pp]roteins?[\s:]+(?P<val>[\d.]+)"],
    "albumin":                   [r"[Aa]lbumin[\s:]+(?P<val>[\d.]+)"],
    "ag_ratio":                  [r"A[/]?G\s*[Rr]atio[\s:]+(?P<val>[\d.]+)"],

    # Thyroid
    "TSH":                       [r"TSH[\s:]+(?P<val>[\d.]+)"],
    "T3":                        [r"\bT3[\s:]+(?P<val>[\d.]+)"],
    "TT4":                       [r"(?:TT4|[Tt]otal\s*T4)[\s:]+(?P<val>[\d.]+)"],
    "FTI":                       [r"FTI[\s:]+(?P<val>[\d.]+)"],
    "T4U":                       [r"T4U[\s:]+(?P<val>[\d.]+)"],

    # Anemia
    "Hemoglobin":                [r"H[ae]moglobin[\s:]+(?P<val>[\d.]+)"],
    "MCH":                       [r"\bMCH\b[\s:]+(?P<val>[\d.]+)"],
    "MCHC":                      [r"\bMCHC\b[\s:]+(?P<val>[\d.]+)"],
    "MCV":                       [r"\bMCV\b[\s:]+(?P<val>[\d.]+)"],
}


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract all text from a PDF file (bytes)."""
    if not PYMUPDF_AVAILABLE:
        return ""
    try:
        doc  = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    except Exception:
        return ""


def extract_fields(pdf_bytes: bytes, disease: str) -> dict:
    """
    Attempt to extract lab values relevant to `disease` from a PDF.

    Returns:
        dict of {feature_key: float_value} for successfully extracted fields.
        Unrecognised fields are simply omitted — form will leave them blank.
    """
    text    = extract_text_from_pdf(pdf_bytes)
    results = {}

    if not text:
        return results

    from utils.constants import DISEASE_FEATURES
    disease_keys = {f["key"] for f in DISEASE_FEATURES.get(disease, [])}

    for key in disease_keys:
        patterns = FIELD_PATTERNS.get(key, [])
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    results[key] = float(match.group("val"))
                    break   # stop at first successful pattern
                except ValueError:
                    continue

    return results


def get_dummy_extracted(disease: str) -> dict:
    """
    Returns a small set of pre-filled dummy values for UI testing.
    Remove this once real PDF extraction is live.
    """
    DUMMY = {
        "diabetes":    {"Glucose": 142, "BloodPressure": 74, "BMI": 31.2, "Age": 48},
        "liver":       {"total_bilirubin": 1.8, "sgpt": 52, "sgot": 44, "albumin": 3.1},
        "kidney":      {"sc": 2.1, "bu": 55, "hemo": 10.4, "bp": 90},
        "hypothyroid": {"TSH": 8.7, "T3": 0.9, "TT4": 55},
        "anemia":      {"Hemoglobin": 9.5, "MCV": 68.0, "MCH": 22.0},
    }
    return DUMMY.get(disease, {})
