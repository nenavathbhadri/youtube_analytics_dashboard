from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from datetime import datetime
import io

styles = getSampleStyleSheet()


def generate_pdf_report(channel_name, report_data, charts=None):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []

    # Title
    elements.append(Paragraph("<b>YouTube Analytics Report</b>", styles["Title"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%d %B %Y %H:%M')}",
        styles["Normal"]
    ))

    elements.append(Paragraph(f"Channel: {channel_name}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # Report Data
    for key, value in report_data.items():

        elements.append(Paragraph(f"<b>{key}</b>", styles["Heading2"]))
        elements.append(Spacer(1, 5))

        if isinstance(value, list):
            for item in value:
                elements.append(
                    Paragraph(f"{item['title']} - {item['views']} views", styles["Normal"])
                )

        elif isinstance(value, dict):
            for k, v in value.items():
                elements.append(
                    Paragraph(f"{k}: {v}", styles["Normal"])
                )

        else:
            elements.append(Paragraph(str(value), styles["Normal"]))

        elements.append(Spacer(1, 10))

    # Charts
    if charts:
        elements.append(Paragraph("<b>Charts</b>", styles["Heading2"]))
        elements.append(Spacer(1, 10))

        for chart in charts:
            img_buffer = io.BytesIO()
            chart.write_image(img_buffer, format="png")
            img_buffer.seek(0)

            elements.append(Image(img_buffer, width=400, height=250))
            elements.append(Spacer(1, 10))

    doc.build(elements)

    buffer.seek(0)
    return buffer