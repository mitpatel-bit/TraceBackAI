
# TraceBack AI - Multi-Agent Workflow

from root_cause_agent import analyze_root_cause
from recommendation_agent import generate_recommendations
from rag import search_knowledge


def investigate_system(cpu_usage, response_time, log_text):
    """
    Coordinate root-cause analysis, knowledge retrieval,
    and recommendation generation.
    """

    # Agent 1: Analyze metrics and system logs
    logs = log_text.splitlines()

    root_cause_result = analyze_root_cause(
        cpu_usage=cpu_usage,
        response_time=response_time,
        log_lines=logs
    )

    # Agent 2: Retrieve related troubleshooting knowledge
    search_question = (
        root_cause_result["probable_cause"]
        + " "
        + log_text
    )

    knowledge_results = search_knowledge(
        search_question,
        top_k=2
    )

    # Agent 3: Generate prioritized recommendations
    recommendations = generate_recommendations(
        root_cause_result
    )

    # Combine all results into one report
    report = {
        "status": root_cause_result["status"],
        "probable_cause": root_cause_result["probable_cause"],
        "evidence": root_cause_result["evidence"],
        "knowledge": knowledge_results,
        "recommendations": recommendations
    }

    return report


# Test the complete workflow
if __name__ == "__main__":
    sample_logs = (
        "ERROR Database connection failed\n"
        "CRITICAL Server response timeout"
    )

    result = investigate_system(
        cpu_usage=97,
        response_time=1200,
        log_text=sample_logs
    )

    print("\nTraceBack AI - Multi-Agent Investigation")
    print("----------------------------------------")
    print("Status:", result["status"])
    print("Probable cause:", result["probable_cause"])

    print("\nEvidence:")
    for item in result["evidence"]:
        print("-", item)

    print("\nRelated Knowledge:")
    for item in result["knowledge"]:
        print("-", item["topic"])
        print(item["content"])

    print("\nPrioritized Recommendations:")
    for item in result["recommendations"]:
        print(
            f"- [{item['priority']}] "
            f"{item['action']}: {item['details']}"
        )
