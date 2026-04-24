# utils/validators.py
# ─────────────────────────────────────────────────────────────────
# Input validation helpers used by the diagnostics form.
# ─────────────────────────────────────────────────────────────────

from utils.constants import DISEASE_FEATURES


def validate_patient_data(patient_data: dict, disease: str) -> tuple[bool, list[str]]:
    """
    Check that all required fields are present and within expected ranges.

    Returns:
        (is_valid: bool, errors: list[str])
    """
    errors = []
    fields = DISEASE_FEATURES.get(disease, [])

    for field in fields:
        key   = field["key"]
        label = field["label"]
        val   = patient_data.get(key)

        if val is None:
            errors.append(f"'{label}' is missing.")
            continue

        if field["type"] in ("number", "slider"):
            try:
                val = float(val)
            except (TypeError, ValueError):
                errors.append(f"'{label}' must be a number.")
                continue

            lo = field.get("min")
            hi = field.get("max")
            if lo is not None and val < lo:
                errors.append(f"'{label}' value {val} is below the minimum ({lo}).")
            if hi is not None and val > hi:
                errors.append(f"'{label}' value {val} exceeds the maximum ({hi}).")

    return (len(errors) == 0), errors


def validate_pdf_extracted_data(extracted: dict, disease: str) -> tuple[dict, list[str]]:
    """
    After PDF extraction, check which required fields were found.
    Returns the cleaned dict and a list of missing field names.
    """
    fields    = DISEASE_FEATURES.get(disease, [])
    required  = {f["key"] for f in fields}
    found     = set(extracted.keys())
    missing   = required - found
    warnings  = [f"Could not extract '{k}' from PDF — please fill in manually." for k in missing]
    return extracted, warnings
