
# TraceBack AI - Recommendation Agent

def generate_recommendations(analysis_result):
    """
    Convert root cause analysis findings into
    prioritized troubleshooting recommendations.
    """

    probable_cause = analysis_result.get(
        "probable_cause", ""
    ).lower()

    evidence = analysis_result.get("evidence", [])

    recommendations = []

    # Priority 1: Critical system problems
    if "timeout" in probable_cause:
        recommendations.append({
            "priority": "High",
            "action": "Investigate server timeout",
            "details": (
                "Check server availability, request delays, "
                "network connectivity, and service logs."
            )
        })

    if "database connection" in probable_cause:
        recommendations.append({
            "priority": "High",
            "action": "Check database connectivity",
            "details": (
                "Verify that the database service is running, "
                "connection settings are correct, and the "
                "database is reachable."
            )
        })

    # Priority 2: Performance problems
    if "high cpu" in probable_cause:
        recommendations.append({
            "priority": "Medium",
            "action": "Investigate high CPU usage",
            "details": (
                "Identify CPU-intensive processes and check "
                "whether system workload has increased."
            )
        })

    if "slow server response" in probable_cause:
        recommendations.append({
            "priority": "Medium",
            "action": "Investigate slow response time",
            "details": (
                "Review application performance, slow database "
                "queries, and network delays."
            )
        })

    # Check for critical log evidence
    critical_evidence = [
        item for item in evidence
        if "critical" in item.lower()
        or "fatal" in item.lower()
    ]

    if critical_evidence:
        recommendations.append({
            "priority": "High",
            "action": "Review critical log entries",
            "details": (
                "Inspect the surrounding log messages and "
                "check which services were affected."
            )
        })

    # Provide a default recommendation when no rules match
    if not recommendations:
        recommendations.append({
            "priority": "Low",
            "action": "Continue system monitoring",
            "details": (
                "Collect additional logs and performance "
                "metrics to investigate further."
            )
        })

    # Remove duplicate actions
    unique_recommendations = []
    seen_actions = set()

    for item in recommendations:
        if item["action"] not in seen_actions:
            unique_recommendations.append(item)
            seen_actions.add(item["action"])

    # Sort recommendations: High, Medium, Low
    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    unique_recommendations.sort(
        key=lambda item: priority_order[item["priority"]]
    )

    return unique_recommendations


# Test the Recommendation Agent independently
if __name__ == "__main__":
    sample_analysis = {
        "probable_cause": (
            "High CPU usage; Very slow server response; "
            "Possible database connection failure; "
            "Possible timeout issue"
        ),
        "evidence": [
            "CPU usage is 97%.",
            "Response time is 1200 milliseconds.",
            "Critical log entry: Server response timeout"
        ]
    }

    results = generate_recommendations(sample_analysis)

    print("\nTraceBack AI - Recommendation Agent")
    print("----------------------------------")

    for number, item in enumerate(results, start=1):
        print(f"\n{number}. Priority: {item['priority']}")
        print("Action:", item["action"])
        print("Details:", item["details"])
