
# TraceBack AI - Root Cause Analysis Agent

def analyze_root_cause(cpu_usage, response_time, log_lines=None):
    """
    Analyze system metrics and logs to identify a likely root cause.
    This version uses rule-based analysis.
    """

    findings = []
    evidence = []
    recommendations = []

    logs = log_lines or []

    # Check CPU usage
    if cpu_usage >= 90:
        findings.append("High CPU usage")
        evidence.append(f"CPU usage is {cpu_usage}%.")
        recommendations.append(
            "Check running processes and stop unnecessary tasks."
        )

    # Check response time
    if response_time >= 800:
        findings.append("Very slow server response")
        evidence.append(
            f"Response time is {response_time} milliseconds."
        )
        recommendations.append(
            "Check server load, database queries, and network delays."
        )
    elif response_time >= 500:
        findings.append("Slow server response")
        evidence.append(
            f"Response time is {response_time} milliseconds."
        )
        recommendations.append(
            "Inspect server performance and recent requests."
        )

    # Analyze log messages
    for line in logs:
        message = line.strip()
        upper_message = message.upper()

        if any(word in upper_message for word in [
            "DATABASE CONNECTION FAILED",
            "DATABASE ERROR",
            "DB CONNECTION FAILED"
        ]):
            findings.append("Possible database connection failure")
            evidence.append(f"Log evidence: {message}")
            recommendations.append(
                "Check database service status, connection settings, "
                "and network connectivity."
            )

        elif "TIMEOUT" in upper_message:
            findings.append("Possible timeout issue")
            evidence.append(f"Log evidence: {message}")
            recommendations.append(
                "Check server response delays, service availability, "
                "and network connectivity."
            )

        elif "CRITICAL" in upper_message or "FATAL" in upper_message:
            evidence.append(f"Critical log entry: {message}")
            recommendations.append(
                "Investigate the critical log entry and inspect "
                "nearby events."
            )

        elif "ERROR" in upper_message or "FAIL" in upper_message:
            evidence.append(f"Error log entry: {message}")
            recommendations.append(
                "Inspect the error details and related application logs."
            )

    # Remove duplicate results while preserving order
    findings = list(dict.fromkeys(findings))
    evidence = list(dict.fromkeys(evidence))
    recommendations = list(dict.fromkeys(recommendations))

    # Prepare final analysis
    if findings:
        probable_cause = "; ".join(findings)
        status = "Potential issue detected"
    elif evidence:
        probable_cause = "Log issues require further investigation"
        status = "Review required"
    else:
        probable_cause = "No obvious issue detected by current rules"
        status = "No obvious issue detected"

    if not recommendations:
        recommendations.append(
            "Continue monitoring system metrics and logs."
        )

    return {
        "status": status,
        "probable_cause": probable_cause,
        "evidence": evidence,
        "recommendations": recommendations
    }


# Run a simple test when this file is executed directly
if __name__ == "__main__":
    result = analyze_root_cause(
        cpu_usage=97,
        response_time=1200,
        log_lines=[
            "ERROR Database connection failed",
            "CRITICAL Server response timeout"
        ]
    )

    print("\nTraceBack AI - Root Cause Analysis")
    print("----------------------------------")
    print("Status:", result["status"])
    print("Probable cause:", result["probable_cause"])

    print("\nEvidence:")
    for item in result["evidence"]:
        print("-", item)

    print("\nRecommendations:")
    for item in result["recommendations"]:
        print("-", item)
