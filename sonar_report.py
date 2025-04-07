import os
import requests

SONAR_TOKEN = os.getenv("SONAR_TOKEN")
SONAR_HOST_URL = os.getenv("SONAR_HOST_URL")
PROJECT_KEY = "Amal.NET"

auth = (SONAR_TOKEN, '')

response = requests.get(
    f"{SONAR_HOST_URL}/api/issues/search?componentKeys={PROJECT_KEY}",
    auth=auth
)

if response.status_code == 200:
    issues = response.json().get("issues", [])
    with open("sonarqube_report.txt", "w") as report_file:
        for issue in issues:
            report_file.write(f"{issue['message']} ({issue['severity']})\n")
    print("Report generated: sonarqube_report.txt")
else:
    print("Failed to fetch issues:", response.status_code, response.text)
