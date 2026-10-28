
# TraceBack AI - Report Generator

from datetime import datetime


def generate_report(report):
    """Create a readable investigation report."""

    lines = [
        "=" * 60,
        "TRACEBACK AI - INVESTIGATION REPORT",
        "=" * 60,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "1. INVESTIGATION SUMMARY",
        f"Status: {report['status']}",
        f"Probable Cause: {report['probable_cause']}",
        "",
        "2. EVIDENCE",
    ]

    for item in report["evidence"]:
        lines.append(f"- {item}")

    lines.extend(["", "3. RELATED TROUBLESHOOTING KNOWLEDGE"])

    if report["knowledge"]:
        for item in report["knowledge"]:
            lines.append(f"\n{item['topic']}")
            lines.append(f"Relevance Score: {item['score']}")
            lines.append(item["content"])
    else:
        lines.append("No related knowledge found.")

    lines.extend(["", "4. PRIORITIZED RECOMMENDATIONS"])

    for item in report["recommendations"]:
        lines.append(
            f"\n[{item['priority']}] {item['action']}"
        )
        lines.append(item["details"])

    lines.extend([
        "",
        "=" * 60,
        "End of Report",
        "=" * 60,
    ])

    return "\n".join(lines)


if __name__ == "__main__":
    sample_report = {
        "status": "Anomaly Detected",
        "probable_cause": "High CPU usage and server timeout",
        "evidence": [
            "CPU usage reached 97%",
            "Response time reached 1200 ms",
            "Critical server timeout found in logs",
        ],
        "knowledge": [],
        "recommendations": [
            {
                "priority": "High",
                "action": "Investigate server timeout",
                "details": "Check service availability and network delays.",
            }
        ],
    }

    output = generate_report(sample_report)

    with open(
        "sample_investigation_report.txt",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(output)

    print(output)
    print("\nReport saved as sample_investigation_report.txt")
