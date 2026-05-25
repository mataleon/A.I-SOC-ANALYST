import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

class AIAnalyst:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def analyze_incident(self, incident_data, alerts_data):
        incident_name = incident_data["properties"].get("title", "Unknown")
        severity = incident_data["properties"].get("severity", "Unknown")
        status = incident_data["properties"].get("status", "Unknown")
        description = incident_data["properties"].get("description", "No description")
        created = incident_data["properties"].get("createdTimeUtc", "Unknown")

        alert_summary = ""
        for alert in alerts_data[:5]:
            props = alert.get("properties", {})
            alert_summary += f"- {props.get('alertDisplayName', 'Alert')}: {props.get('description', '')}\n"

        prompt = f"""You are an expert SOC analyst with 10 years of experience.
Analyze this Microsoft Sentinel security incident and provide a detailed investigation report.

INCIDENT DETAILS:
- Title: {incident_name}
- Severity: {severity}
- Status: {status}
- Created: {created}
- Description: {description}

ASSOCIATED ALERTS:
{alert_summary if alert_summary else 'No alerts available'}

Provide your analysis in this exact format:

## INCIDENT SUMMARY
[2-3 sentence summary of what happened]

## THREAT ASSESSMENT
- Severity Justification: [why this severity is appropriate]
- Threat Actor Profile: [type of attacker]
- Attack Stage: [where in the kill chain]

## TECHNICAL ANALYSIS
[Detailed technical explanation of the attack]

## MITRE ATT&CK MAPPING
[Specific techniques involved]

## IMPACT ASSESSMENT
- Immediate Risk: [what could happen now]
- Potential Impact: [worst case scenario]
- Affected Systems: [what is at risk]

## INVESTIGATION STEPS
1. [First thing to check]
2. [Second thing to check]
3. [Third thing to check]
4. [Fourth thing to check]
5. [Fifth thing to check]

## RECOMMENDED RESPONSE
- Immediate Actions: [urgent steps]
- Short Term: [remediation steps]
- Long Term: [hardening recommendations]

## VERDICT
Classification: [True Positive / False Positive / Benign Positive]
Confidence: [High/Medium/Low]
Priority: [Critical/High/Medium/Low]"""

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    def ask_followup(self, incident_context, question):
        prompt = f"""You are an expert SOC analyst.
Context: {incident_context}
Question: {question}
Answer as a senior SOC analyst — specific, technical and actionable."""

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text