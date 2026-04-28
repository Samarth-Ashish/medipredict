# components/report.py
# ─────────────────────────────────────────────────────────────────
# Generates a nicely formatted PDF diagnostic report using fpdf2.
# Call  generate_report_pdf()  after a prediction is complete.
# ─────────────────────────────────────────────────────────────────

from datetime import datetime
import io

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False


def generate_report_pdf(
    patient_info: dict,
    result: dict,
    disease_label: str,
    patient_data: dict,
) -> bytes | None:
    """
    Build a PDF report and return it as bytes (for st.download_button).

    Args:
        patient_info  : {"name": str, "age": int, "gender": str, "report_id": str}
        result        : dict returned by predictor.predict_disease()
        disease_label : Human-readable disease name (e.g. "Diabetes")
        patient_data  : Raw input feature dict

    Returns:
        PDF bytes, or None if fpdf2 is not installed.
    """
    if not FPDF_AVAILABLE:
        return None

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ── Header ─────────────────────────────────────────────────────
    pdf.set_fill_color(10, 15, 30)
    pdf.rect(0, 0, 210, 35, "F")

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(0, 180, 216)
    pdf.set_y(8)
    pdf.cell(0, 10, "MediPredict AI", align="C", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(200, 210, 230)
    pdf.cell(0, 8, "AI-Assisted Diagnostic Report  |  For Medical Reference Only", align="C", ln=True)

    pdf.set_text_color(0, 0, 0)
    pdf.ln(12)

    # ── Report metadata ────────────────────────────────────────────
    pdf.set_fill_color(240, 245, 255)
    pdf.rect(10, pdf.get_y(), 190, 28, "F")

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(20, 30, 70)
    pdf.set_x(14)
    pdf.cell(0, 7, f"Patient: {patient_info.get('name', 'Anonymous')}", ln=True)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_x(14)
    pdf.cell(90, 6, f"Report ID : {patient_info.get('report_id', 'N/A')}")
    pdf.cell(90, 6, f"Date      : {datetime.now().strftime('%d %b %Y, %H:%M')}", ln=True)
    pdf.set_x(14)
    pdf.cell(90, 6, f"Age       : {patient_info.get('age', 'N/A')}")
    pdf.cell(90, 6, f"Gender    : {patient_info.get('gender', 'N/A')}", ln=True)
    pdf.set_x(14)
    pdf.cell(90, 6, f"Disease   : {disease_label}")
    pdf.cell(90, 6, f"Screened by: MediPredict AI v1.0", ln=True)

    pdf.ln(6)

    # ── Result banner ──────────────────────────────────────────────
    prediction  = result.get("prediction", 0)
    risk_level  = result.get("risk_level", "UNKNOWN")
    confidence  = result.get("confidence", 0.0)

    if prediction == 1:
        banner_r, banner_g, banner_b = 200, 40, 40
        result_text = f"POSITIVE - {disease_label} Detected"
    else:
        banner_r, banner_g, banner_b = 30, 150, 80
        result_text = f"NEGATIVE - No {disease_label} Detected"

    pdf.set_fill_color(banner_r, banner_g, banner_b)
    pdf.rect(10, pdf.get_y(), 190, 18, "F")
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(255, 255, 255)
    pdf.set_x(14)
    pdf.cell(0, 18, result_text, ln=True)

    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # ── Confidence & risk ──────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(95, 8, f"Confidence Score : {confidence:.1f}%")
    pdf.cell(95, 8, f"Risk Level       : {risk_level}", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 5,
        f"Decision threshold: {result.get('threshold_used', 0.45):.2f}  |  "
        f"Model: XGBoost",
        ln=True,
    )

    if result.get("is_dummy"):
        pdf.set_text_color(200, 80, 0)
        pdf.set_font("Helvetica", "I", 8)
        pdf.cell(0, 5, "⚠  DEMO MODE - Model files not yet loaded. Results are illustrative only.", ln=True)

    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # ── Input values table ─────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Patient Input Values", ln=True)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(220, 230, 245)
    pdf.cell(80, 7, "Parameter", border=1, fill=True)
    pdf.cell(50, 7, "Value", border=1, fill=True)
    pdf.cell(60, 7, "Notes", border=1, fill=True, ln=True)

    pdf.set_font("Helvetica", "", 9)
    fill = False
    for key, val in patient_data.items():
        if pdf.get_y() > 260:
            pdf.add_page()
        pdf.set_fill_color(245, 248, 255) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.cell(80, 6, str(key).replace("_", " ").title(), border=1, fill=fill)
        pdf.cell(50, 6, str(val), border=1, fill=fill)
        pdf.cell(60, 6, "", border=1, fill=fill, ln=True)
        fill = not fill

    pdf.ln(6)

    # ── Feature importance (if present) ───────────────────────────
    importance = result.get("feature_importance", [])
    if importance:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Key Influencing Factors (AI Explanation)", ln=True)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(220, 230, 245)
        pdf.cell(70, 7, "Feature", border=1, fill=True)
        pdf.cell(40, 7, "Your Value", border=1, fill=True)
        pdf.cell(40, 7, "Impact", border=1, fill=True)
        pdf.cell(40, 7, "Direction", border=1, fill=True, ln=True)

        pdf.set_font("Helvetica", "", 9)
        for row in importance[:6]:
            impact    = row.get("impact", 0)
            direction = "↑ Increases risk" if impact > 0 else "↓ Reduces risk"
            pdf.cell(70, 6, str(row.get("feature", "")), border=1)
            pdf.cell(40, 6, str(row.get("value", "")), border=1)
            pdf.cell(40, 6, f"{impact:+.3f}", border=1)
            pdf.cell(40, 6, direction, border=1, ln=True)

        pdf.ln(6)

    # ── Disclaimer ────────────────────────────────────────────────
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(130, 130, 130)
    disclaimer = (
        "DISCLAIMER: This report is generated by an AI model for educational and screening purposes only. "
        "It does NOT constitute a medical diagnosis. Please consult a qualified healthcare professional "
        "for clinical interpretation and treatment decisions. Do not make any medical decisions based "
        "solely on this output."
    )
    pdf.multi_cell(0, 4, disclaimer)

    # Return as bytes
    return bytes(pdf.output())
