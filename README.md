 AI SOC Analyst
Automated Security Incident Investigation Powered by Claude AI + Microsoft Sentinel 📌 Overview
AI SOC Analyst is an intelligent security operations tool that connects directly to Microsoft Sentinel, retrieves real security incidents, and uses Claude AI to automatically investigate, analyze and generate professional incident reports — just like a Tier 1 SOC analyst would.
Instead of manually reviewing hundreds of alerts, this tool lets you select any incident and get an instant AI-powered investigation including threat assessment, MITRE ATT&CK mapping, investigation steps and recommended response actions.

🎯 What It Does

Connects to Microsoft Sentinel via Azure API and retrieves live incidents
Analyzes incidents with Claude AI — produces detailed investigation reports in seconds
Generates professional reports in both Markdown and HTML format
Supports interactive Q&A — ask followup questions to the AI analyst
Color-coded terminal interface — incidents displayed by severity (Red/Yellow/Green)


🏗️ Architecture
Microsoft Sentinel
        ↓
   Azure REST API
        ↓
 sentinel_client.py  ←→  .env (credentials)
        ↓
   ai_analyst.py     ←→  Claude AI (Anthropic API)
        ↓
report_generator.py
        ↓
  HTML + MD Reports

📂 Project Structure
ai-soc-analyst/
├── main.py                 ← Main application entry point
├── sentinel_client.py      ← Microsoft Sentinel API connection
├── ai_analyst.py           ← Claude AI analysis engine
├── report_generator.py     ← HTML and Markdown report generator
├── .env                    ← API credentials (never commit this)
├── .gitignore              ← Excludes .env and reports
├── requirements.txt        ← Python dependencies
├── reports/                ← Generated incident reports (auto-created)
└── README.md

⚙️ Installation
Prerequisites

Python 3.13+
Microsoft Azure account with Sentinel workspace
Anthropic API key

Step 1 — Clone the repository
bashgit clone https://github.com/yourusername/ai-soc-analyst
cd ai-soc-analyst
Step 2 — Install dependencies
bashpip install -r requirements.txt
Step 3 — Configure credentials
Create a .env file in the project root:
envANTHROPIC_API_KEY=sk-ant-your-key-here
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_SUBSCRIPTION_ID=your-subscription-id
SENTINEL_WORKSPACE=your-workspace-name
SENTINEL_RESOURCE_GROUP=your-resource-group
Step 4 — Configure Azure permissions
Register an app in Microsoft Entra ID and assign it the Microsoft Sentinel Reader role on your Log Analytics Workspace.
Step 5 — Run
bashpython main.py

🚀 Usage
╔══════════════════════════════════════════╗
║      🤖 AI SOC ANALYST v1.0              ║
║      Powered by Claude + Sentinel        ║
╚══════════════════════════════════════════╝

Connecting to Microsoft Sentinel...
Connected! Fetching incidents...

Recent Incidents (10 found):
============================================================
[1] HIGH | Brute Force Attack Detected
    Status: New | Created: 2026-05-24
[2] HIGH | AD Brute Force Against Domain Accounts
    Status: New | Created: 2026-05-24
[3] HIGH | DCSync Attack Detected
    Status: New | Created: 2026-05-24
============================================================

Enter incident number to analyze (or q to quit): 1

🤖 AI is analyzing the incident...

============================================================
## INCIDENT SUMMARY
A sustained brute force attack was detected targeting the
domain administrator account from IP 148.251.140.16...

## THREAT ASSESSMENT
- Severity Justification: High severity is appropriate given
  the volume of attempts (63,784) and targeting of privileged accounts
- Threat Actor Profile: Automated botnet conducting credential
  stuffing against exposed RDP services
- Attack Stage: Initial Access — attempting to gain foothold

## MITRE ATT&CK MAPPING
- T1110 — Brute Force
- T1110.001 — Password Guessing
- T1078 — Valid Accounts (if successful)
...
============================================================

Save report? (y/n): y
Reports saved to /reports folder!

Ask followup question (or back): Should I block this IP?

🤖 AI Response:
Yes — immediately block 148.251.140.16 at your perimeter
firewall and NSG level. This IP has made 63,784 failed
login attempts which constitutes a clear malicious pattern...

📊 AI Analysis Output
Each incident analysis includes:
SectionDescriptionIncident Summary2-3 sentence overview of what happenedThreat AssessmentSeverity justification, actor profile, kill chain stageTechnical AnalysisDetailed explanation of the attack techniqueMITRE ATT&CK MappingSpecific tactics and techniquesImpact AssessmentImmediate risk, potential impact, affected systemsInvestigation Steps5 specific steps to investigate furtherRecommended ResponseImmediate, short-term and long-term actionsVerdictTrue/False Positive classification with confidence

📄 Sample Report Output
Reports are auto-saved in two formats:
Markdown (reports/incident_report_20260524_223015.md)
HTML (reports/incident_report_20260524_223015.html)
The HTML report opens in any browser with color-coded severity indicators and formatted analysis sections.

🔧 Tech Stack
ComponentTechnologyAI EngineClaude Sonnet (Anthropic API)SIEMMicrosoft SentinelCloudMicrosoft AzureLanguagePython 3.13AuthAzure OAuth2 Client CredentialsReportsMarkdown + HTML

🛡️ Security Notes

Never commit .env — contains API keys and secrets
The app uses read-only Sentinel Reader permissions — cannot modify incidents
API keys should be rotated regularly
All reports saved locally — no data sent to third parties except Anthropic API

Built as part of a cybersecurity portfolio demonstrating AI + security engineering skills.
Powered by Claude AI (Anthropic) + Microsoft Sentinel
