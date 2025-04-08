import os
import requests
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

SONAR_TOKEN = os.getenv("SONAR_TOKEN")
sonarqube_url = os.getenv("SONARQUBE_URL")
PROJECT_KEY = "Amal.NET"

print("SonarQube URL from env:", sonarqube_url)
print("SonarQube Token set:", "YES" if SONAR_TOKEN else "NO")

auth = (SONAR_TOKEN, '')

response = requests.get(
    f"{sonarqube_url}/api/issues/search?componentKeys={PROJECT_KEY}",
    auth=auth
)

if response.status_code == 200:
    issues = response.json().get("issues", [])
    
    # Prepare the PDF
    pdf_filename = "sonarqube_report.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("SonarQube Static Analysis Report", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Project Key: {PROJECT_KEY}", styles['Heading3']))
    story.append(Spacer(1, 12))

    table_data = [['Severity', 'Type', 'Rule', 'File', 'Line', 'Message']]
    
    for issue in issues:
        severity = issue.get('severity', 'N/A')
        issue_type = issue.get('type', 'N/A')
        rule = issue.get('rule', 'N/A')
        file_path = issue.get('component', 'N/A').split(':')[-1]
        line = str(issue.get('line', 'N/A'))
        message = issue.get('message', 'N/A')

        table_data.append([severity, issue_type, rule, file_path, line, message])

    # Style the table
    table = Table(table_data, repeatRows=1, colWidths=[60, 60, 80, 140, 40, 160])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.gray),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    story.append(table)
    doc.build(story)
    print(f"✅ PDF report generated: {pdf_filename}")

else:
    print("❌ Failed to fetch issues:", response.status_code, response.text)

