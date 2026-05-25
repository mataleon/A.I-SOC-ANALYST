import os
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        os.makedirs("reports", exist_ok=True)

    def save_report(self, incident_data, analysis, filename=None):
        incident_name = incident_data["properties"].get("title", "Unknown")
        severity = incident_data["properties"].get("severity", "Unknown")
        created = incident_data["properties"].get("createdTimeUtc", "Unknown")
        incident_id = incident_data.get("name", "Unknown")
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/incident_report_{timestamp}.md"
        report = f"""# SOC Incident Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Title: {incident_name}
Severity: {severity}
Created: {created}

## AI Analysis
{analysis}

Powered by Claude AI + Microsoft Sentinel
"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved: {filename}")
        return filename

    def save_html_report(self, incident_data, analysis):
        incident_name = incident_data["properties"].get("title", "Unknown")
        severity = incident_data["properties"].get("severity", "Unknown")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/incident_report_{timestamp}.html"
        severity_colors = {"High": "#dc3545","Medium": "#fd7e14","Low": "#28a745","Informational": "#17a2b8"}
        color = severity_colors.get(severity, "#6c757d")
        analysis_html = analysis.replace("\n", "<br>")
        html = f"""<!DOCTYPE html>
<html><head><title>SOC Report</title>
<style>body{{font-family:Arial;max-width:900px;margin:40px auto;padding:20px}}
.header{{background:#1a1a2e;color:white;padding:20px;border-radius:8px}}
.severity{{background:{color};color:white;padding:4px 12px;border-radius:4px}}
.analysis{{background:#f8f9fa;padding:20px;border-radius:8px;margin-top:20px}}</style>
</head><body>
<div class="header"><h1>AI SOC Analyst Report</h1>
<h2>{incident_name}</h2>
<span class="severity">Severity: {severity}</span>
<p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p></div>
<div class="analysis">{analysis_html}</div>
</body></html>"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML Report saved: {filename}")
        return filename