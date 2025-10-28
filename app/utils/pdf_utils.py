from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_fuel_plan_pdf(plan_data, runner_info):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("Marathon Fuel Plan", styles["h1"]))
    story.append(
        Paragraph(f"Target Time: {runner_info['target_time']}", styles["BodyText"])
    )
    story.append(Paragraph(f"Distance: {runner_info['distance']}", styles["BodyText"]))
    story.append(Paragraph(f"Weight: {runner_info['weight']}", styles["BodyText"]))
    story.append(Paragraph("<br/><br/>Race Timeline", styles["h2"]))
    timeline_table_data = [["Time", "Action", "Carbs", "Calories", "Sodium"]]
    for item in plan_data:
        timeline_table_data.append(
            [
                item["time_str"],
                item["amount"],
                f"{item['carbs']}g",
                f"{item['calories']}k",
                f"{item['sodium']}mg",
            ]
        )
    timeline_table = Table(timeline_table_data)
    timeline_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    story.append(timeline_table)
    total_carbs = sum((item["carbs"] for item in plan_data))
    total_calories = sum((item["calories"] for item in plan_data))
    total_sodium = sum((item["sodium"] for item in plan_data))
    total_cost = sum((item.get("cost", 0) for item in plan_data))
    story.append(Paragraph("<br/><br/>Plan Summary", styles["h2"]))
    summary_text = f"Total Carbs: {total_carbs}g | Total Calories: {total_calories}kCal | Total Sodium: {total_sodium}mg | Est. Cost: ${total_cost:.2f}"
    story.append(Paragraph(summary_text, styles["BodyText"]))
    story.append(Paragraph("<br/><br/>Race Day Checklist", styles["h2"]))
    checklist_items = [
        "Lay out race kit the night before.",
        "Charge GPS watch and phone.",
        "Prepare pre-race breakfast.",
        "Pack all your fuel items.",
        "Check weather forecast and adjust plan if needed.",
        "Stay hydrated throughout the day before.",
        "Get a good night's sleep!",
    ]
    for item in checklist_items:
        story.append(Paragraph(f"[  ] {item}", styles["Normal"]))
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()