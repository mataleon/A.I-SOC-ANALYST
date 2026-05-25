import os
import sys
from datetime import datetime
from sentinel_client import SentinelClient
from ai_analyst import AIAnalyst
from report_generator import ReportGenerator


def print_banner():
    print("\n" + "="*60)
    print("       AI SOC ANALYST — Powered by Claude + Sentinel")
    print("="*60 + "\n")


def print_incident_summary(incidents):
    print(f"Found {len(incidents)} incident(s):\n")
    for i, inc in enumerate(incidents):
        props = inc.get("properties", {})
        title = props.get("title", "Unknown")
        severity = props.get("severity", "Unknown")
        status = props.get("status", "Unknown")
        created = props.get("createdTimeUtc", "Unknown")[:19].replace("T", " ")
        print(f"  [{i+1}] {title}")
        print(f"       Severity: {severity} | Status: {status} | Created: {created}")
    print()


def process_incident(incident, sentinel, analyst, reporter):
    props = incident.get("properties", {})
    incident_id = incident.get("name", "unknown")
    title = props.get("title", "Unknown Incident")
    severity = props.get("severity", "Unknown")

    print(f"\n{'─'*60}")
    print(f"  Analyzing: {title}")
    print(f"  Severity:  {severity}")
    print(f"{'─'*60}")

    print("  [1/3] Fetching associated alerts...")
    try:
        alerts = sentinel.get_incident_alerts(incident_id)
        print(f"         Found {len(alerts)} alert(s)")
    except Exception as e:
        print(f"         Warning: Could not fetch alerts — {e}")
        alerts = []

    print("  [2/3] Running AI analysis...")
    try:
        analysis = analyst.analyze_incident(incident, alerts)
        print("         Analysis complete")
    except Exception as e:
        print(f"         Error during analysis: {e}")
        return None, None

    print("  [3/3] Saving reports...")
    try:
        md_file = reporter.save_report(incident, analysis)
        html_file = reporter.save_html_report(incident, analysis)
        print(f"         Markdown : {md_file}")
        print(f"         HTML     : {html_file}")
    except Exception as e:
        print(f"         Error saving reports: {e}")
        return analysis, None

    return analysis, html_file


def run_interactive_mode(incident, analysis, analyst):
    props = incident.get("properties", {})
    title = props.get("title", "this incident")
    context = f"Incident: {title}\n\nAnalysis:\n{analysis}"

    print(f"\n  Interactive mode — ask follow-up questions about this incident.")
    print("  Type 'done' to move to the next incident, 'quit' to exit.\n")

    while True:
        try:
            question = input("  Your question: ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if question.lower() in ("done", "next", ""):
            break
        if question.lower() in ("quit", "exit", "q"):
            sys.exit(0)

        print("\n  Thinking...\n")
        try:
            answer = analyst.ask_followup(context, question)
            print(f"  {answer}\n")
        except Exception as e:
            print(f"  Error: {e}\n")


def main():
    print_banner()

    # Parse args: python main.py [--limit N] [--interactive]
    limit = 5
    interactive = False
    args = sys.argv[1:]
    if "--limit" in args:
        idx = args.index("--limit")
        try:
            limit = int(args[idx + 1])
        except (IndexError, ValueError):
            pass
    if "--interactive" in args or "-i" in args:
        interactive = True

    print("Connecting to Microsoft Sentinel...")
    try:
        sentinel = SentinelClient()
        print("Connected.\n")
    except Exception as e:
        print(f"Failed to connect to Sentinel: {e}")
        sys.exit(1)

    analyst = AIAnalyst()
    reporter = ReportGenerator()

    print(f"Fetching last {limit} incident(s)...")
    try:
        incidents = sentinel.get_incidents(limit=limit)
    except Exception as e:
        print(f"Failed to fetch incidents: {e}")
        sys.exit(1)

    if not incidents:
        print("No incidents found in your Sentinel workspace.")
        sys.exit(0)

    print_incident_summary(incidents)

    processed = 0
    for incident in incidents:
        analysis, html_file = process_incident(incident, sentinel, analyst, reporter)

        if analysis and interactive:
            run_interactive_mode(incident, analysis, analyst)

        if analysis:
            processed += 1

    print(f"\n{'='*60}")
    print(f"  Done. Processed {processed}/{len(incidents)} incident(s).")
    print(f"  Reports saved to: {os.path.abspath('reports')}/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
