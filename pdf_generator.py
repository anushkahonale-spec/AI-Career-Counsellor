from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data, filename="career_report.pdf"):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>AI CAREER COUNSELLOR REPORT</b>", styles['Title']))
    elements.append(Paragraph("<br/>", styles['Normal']))

    elements.append(Paragraph(f"<b>Name:</b> {data['name']}", styles['Normal']))
    elements.append(Paragraph(f"<b>Recommended Career:</b> {data['career']}", styles['Normal']))
    elements.append(Paragraph(f"<b>Career Match:</b> {data['score']}%", styles['Normal']))
    elements.append(Paragraph(f"<b>Expected Salary:</b> {data['salary']}", styles['Normal']))

    elements.append(Paragraph("<br/><b>Top Companies</b>", styles['Heading2']))

    for company in data["companies"]:
        elements.append(Paragraph(f"• {company}", styles['Normal']))

    elements.append(Paragraph("<br/><b>Skills To Learn</b>", styles['Heading2']))

    for skill in data["skills"]:
        elements.append(Paragraph(f"• {skill}", styles['Normal']))

    elements.append(Paragraph("<br/><b>Career Roadmap</b>", styles['Heading2']))

    for step in data["roadmap"]:
        elements.append(Paragraph(f"✔ {step}", styles['Normal']))

    elements.append(Paragraph("<br/><b>AI Recommendation</b>", styles['Heading2']))
    elements.append(Paragraph(data["why"], styles['Normal']))

    doc.build(elements)

    return filename