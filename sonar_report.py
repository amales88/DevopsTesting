import os
import requests
from weasyprint import HTML

SONAR_TOKEN = os.getenv("SONAR_TOKEN")
sonarqube_url = os.getenv("SONARQUBE_URL")
PROJECT_KEY = "Amal.NET"

auth = (SONAR_TOKEN, '')

# Fetch issues
issues_url = f"{SONAR_HOST_URL}/api/issues/search?componentKeys={PROJECT_KEY}"
metrics_url = f"{SONAR_HOST_URL}/api/measures/component?component={PROJECT_KEY}&metricKeys=bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density,ncloc,security_hotspots,security_review_rating"

issues_resp = requests.get(issues_url, auth=auth)
metrics_resp = requests.get(metrics_url, auth=auth)

if issues_resp.status_code != 200 or metrics_resp.status_code != 200:
    print("Failed to fetch data")
    print("Issues status:", issues_resp.status_code)
    print("Metrics status:", metrics_resp.status_code)
    exit(1)

issues = issues_resp.json().get("issues", [])
metrics = metrics_resp.json().get("component", {}).get("measures", [])

# Prepare metric dict
metric_dict = {m["metric"]: m["value"] for m in metrics}

# Convert to UI-friendly data
def display(value, default="–"):
    return value if value else default

bugs = display(metric_dict.get("bugs", "0"))
vulnerabilities = display(metric_dict.get("vulnerabilities", "0"))
hotspots = display(metric_dict.get("security_hotspots", "–"))
code_smells = display(metric_dict.get("code_smells", "0"))
coverage = display(metric_dict.get("coverage", "0.0%")) + "%"
duplication = display(metric_dict.get("duplicated_lines_density", "0.0")) + "%"
lines = display(metric_dict.get("ncloc", "0"))

# HTML report
html = f"""
<html>
<head>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background-color: #f4f6f9;
      padding: 20px;
    }}
    .title {{
      font-size: 28px;
      font-weight: bold;
      color: #333;
    }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
      margin-top: 20px;
    }}
    .card {{
      background: white;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
      text-align: center;
    }}
    .card h2 {{
      margin: 0;
      font-size: 20px;
      color: #666;
    }}
    .card p {{
      font-size: 24px;
      font-weight: bold;
      margin-top: 10px;
      color: #111;
    }}
    .issues {{
      margin-top: 40px;
    }}
    .issue {{
      padding: 10px;
      border-bottom: 1px solid #ccc;
    }}
    .issue:last-child {{
      border-bottom: none;
    }}
    .severity-CRITICAL {{ color: #e31e1e; font-weight: bold; }}
    .severity-MAJOR {{ color: #e67e22; }}
    .severity-MINOR {{ color: #3498db; }}
  </style>
</head>
<body>
  <div class="title">SonarQube Project Report - {PROJECT_KEY}</div>

  <div class="summary">
    <div class="card"><h2>Bugs</h2><p>{bugs}</p></div>
    <div class="card"><h2>Vulnerabilities</h2><p>{vulnerabilities}</p></div>
    <div class="card"><h2>Hotspots Reviewed</h2><p>{hotspots}</p></div>
    <div class="card"><h2>Code Smells</h2><p>{code_smells}</p></div>
    <div class="card"><h2>Coverage</h2><p>{coverage}</p></div>
    <div class="card"><h2>Duplications</h2><p>{duplication}</p></div>
    <div class="card"><h2>Lines</h2><p>{lines}</p></div>
  </div>

  <div class="issues">
    <h2>Issues</h2>
    {''.join(f'<div class="issue severity-{issue["severity"]}">{issue["message"]} ({issue["severity"]})</div>' for issue in issues)}
  </div>
</body>
</html>
"""

# Save to PDF
HTML(string=html).write_pdf("sonarqube_report.pdf")
print("✅ PDF Report Generated: sonarqube_report.pdf")


