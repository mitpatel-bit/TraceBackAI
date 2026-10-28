
import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
from multi_agent_workflow import investigate_system
from report_generator import generate_report

st.set_page_config(page_title="TraceBack AI", page_icon="🔍", layout="wide")

st.title("🔍 TraceBack AI")
st.subheader("Multi-Agent Root Cause Investigator")
st.write("Detect unusual system activity using machine learning.")

# Sample system data
data = {
    "Time": ["10:00", "10:01", "10:02", "10:03", "10:04",
             "10:05", "10:06", "10:07", "10:08", "10:09"],
    "CPU Usage (%)": [35, 38, 42, 40, 45, 48, 94, 97, 43, 41],
    "Response Time (ms)": [120, 125, 135, 130, 145, 150,
                           850, 1200, 140, 135]
}

df = pd.DataFrame(data)

# Machine learning anomaly detection
features = df[["CPU Usage (%)", "Response Time (ms)"]]

model = IsolationForest(contamination=0.2, random_state=42)
df["Prediction"] = model.fit_predict(features)

df["Status"] = df["Prediction"].map({
    1: "Normal",
    -1: "Anomaly"
})

anomalies = int((df["Status"] == "Anomaly").sum())

# Dashboard metrics

# Dashboard metrics
col1, col2, col3 = st.columns(3)

col1.metric("Latest CPU Usage", f"{df.iloc[-1]['CPU Usage (%)']}%")
col2.metric(
    "Latest Response Time",
    f"{df.iloc[-1]['Response Time (ms)']} ms"
)
col3.metric("Detected Anomalies", anomalies)


# System Health Overview - PASTE HERE
st.subheader("📊 System Health Overview")

chart_data = pd.DataFrame({
    "Metric": ["CPU Usage (%)", "Response Time (ms)"],
    "Current Value": [
        df.iloc[-1]["CPU Usage (%)"],
        df.iloc[-1]["Response Time (ms)"]
    ]
})

st.bar_chart(
    chart_data,
    x="Metric",
    y="Current Value"
)


# Data table
st.subheader("📊 System Monitoring Data")
st.dataframe(
    df.drop(columns=["Prediction"]),
    use_container_width=True
)

# Data table

st.subheader("📊 System Monitoring Data")
st.dataframe(
    df.drop(columns=["Prediction"]),
    use_container_width=True
)

# Anomaly results

st.subheader("🚨 Anomaly Detection Summary")

total_records = len(df)
anomaly_count = int((df["Prediction"] == -1).sum())
normal_count = int((df["Prediction"] == 1).sum())

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", total_records)
col2.metric("Anomalies Found", anomaly_count)
col3.metric("Normal Records", normal_count)

if anomaly_count > 0:
    st.warning(
        f"{anomaly_count} anomalous record(s) detected. "
        "Review the records below."
    )
else:
    st.success("No anomalies detected in the current dataset.")

st.subheader("🚨 Anomaly Detection Results")

if anomalies > 0:
    st.warning(f"The model detected {anomalies} unusual data points.")
    st.dataframe(
        df[df["Status"] == "Anomaly"][
            ["Time", "CPU Usage (%)", "Response Time (ms)", "Status"]
        ],
        use_container_width=True
    )
else:
    st.success("No anomalies detected.")

# Charts
st.subheader("CPU Usage Over Time")
st.line_chart(df.set_index("Time")["CPU Usage (%)"])

st.subheader("Response Time Over Time")
st.line_chart(df.set_index("Time")["Response Time (ms)"])

st.info("This is a demonstration using sample data, not live system monitoring.")


# ---------------------------------
# PART 2: SYSTEM LOG ANALYSIS
# ---------------------------------

st.header("📝 2. System Log Analysis")

st.write(
    "Upload a text or log file to identify important messages "
    "and possible system problems."
)

uploaded_file = st.file_uploader(
    "Upload a system log file",
    type=["txt", "log"]
)

if uploaded_file is not None:
    try:
        log_text = uploaded_file.getvalue().decode(
            "utf-8",
            errors="replace"
        )

        log_lines = log_text.splitlines()
        results = []

        for line_number, line in enumerate(log_lines, start=1):
            upper_line = line.upper()

            if "CRITICAL" in upper_line or "FATAL" in upper_line:
                level = "CRITICAL"
            elif "ERROR" in upper_line or "FAIL" in upper_line:
                level = "ERROR"
            elif "WARNING" in upper_line or "WARN" in upper_line:
                level = "WARNING"

            else:
                continue

            results.append({
                "Line": line_number,
                "Level": level,
                "Message": line
            })

        st.subheader("Log Analysis Summary")

        col1, col2 = st.columns(2)
        col1.metric("Total Log Lines", len(log_lines))
        col2.metric("Important Messages", len(results))

        if results:
            results_df = pd.DataFrame(results)

            critical_count = sum(
                1 for item in results
                if item["Level"] == "CRITICAL"
            )

            error_count = sum(
                1 for item in results
                if item["Level"] == "ERROR"
            )

            warning_count = sum(
                1 for item in results
                if item["Level"] == "WARNING"
            )

            col1, col2, col3 = st.columns(3)
            col1.metric("Critical Messages", critical_count)
            col2.metric("Errors", error_count)
            col3.metric("Warnings", warning_count)

            st.subheader("Detected Log Issues")
            st.dataframe(results_df, use_container_width=True)

        else:
            st.success(
                "No ERROR, WARNING, or CRITICAL messages found."
            )

    except Exception as error:
        st.error(f"Could not analyze the uploaded file: {error}")

else:
    st.info("Upload a .txt or .log file to begin log analysis.")

st.caption(
    "Log analysis currently uses keyword matching on uploaded sample "
    "or real logs. Live system monitoring is not connected yet."
)


# ---------------------------------
# PART 3: RAG KNOWLEDGE SEARCH
# ---------------------------------

from rag import search_knowledge

st.header("🧠 3. Troubleshooting Knowledge Search")

st.write(
    "Ask a question to retrieve relevant information "
    "from the troubleshooting knowledge base."
)

question = st.text_input(
    "Enter your troubleshooting question",
    placeholder="Example: Why is my database connection failing?"
)

if st.button("Search Knowledge"):
    if question.strip():
        try:
            results = search_knowledge(question, top_k=2)

            if results:
                st.subheader("Relevant Knowledge")

                for i, result in enumerate(results, start=1):
                    with st.expander(
                        f"Result {i}: {result['topic']}"
                    ):
                        st.caption(
                            f"Relevance score: {result['score']}"
                        )
                        st.text(result["content"])
            else:
                st.info(
                    "No relevant information found. "
                    "Try different keywords."
                )

        except Exception as error:
            st.error(f"Knowledge search failed: {error}")
    else:
        st.warning("Please enter a question first.")


# ---------------------------------
# PART 4: ROOT CAUSE ANALYSIS AGENT
# ---------------------------------

from root_cause_agent import analyze_root_cause
from recommendation_agent import generate_recommendations
st.header("🔎 4. Root Cause Analysis Agent")

st.write(
    "Analyze system metrics and log messages to identify "
    "possible causes and recommended actions."
)

cpu_input = st.number_input(
    "CPU Usage (%)",
    min_value=0.0,
    max_value=100.0,
    value=97.0,
    step=1.0
)

response_input = st.number_input(
    "Response Time (milliseconds)",
    min_value=0,
    max_value=60000,
    value=1200,
    step=50
)

log_input = st.text_area(
    "Enter system log messages (one per line)",
    value=(
        "ERROR Database connection failed\n"
        "CRITICAL Server response timeout"
    ),
    height=130
)

if st.button("Investigate Root Cause"):
    try:
        logs = log_input.splitlines()

        result = analyze_root_cause(
            cpu_usage=cpu_input,
            response_time=response_input,
            log_lines=logs
        )

        st.subheader("Investigation Results")

        st.write("**Status:**", result["status"])
        st.write("**Probable Cause:**", result["probable_cause"])

        st.subheader("Evidence Found")

        if result["evidence"]:
            for item in result["evidence"]:
                st.write("•", item)
        else:
            st.info("No specific evidence found.")

        st.subheader("Recommended Actions")

        for item in result["recommendations"]:
            st.write("•", item)

        st.caption(
            "These are rule-based findings. Verify the evidence "
            "before deciding on the actual root cause."
        )

    except Exception as error:
        st.error(f"Root cause analysis failed: {error}")


# Multi-Agent Investigation Workflow

st.header("🤖 5. Multi-Agent Investigation Workflow")

st.write(
    "Run root-cause analysis, knowledge retrieval, "
    "and recommendations together."
)

workflow_cpu = st.number_input(
    "Workflow CPU Usage (%)",
    min_value=0.0,
    max_value=100.0,
    value=97.0,
    step=1.0,
    key="workflow_cpu"
)

workflow_response = st.number_input(
    "Workflow Response Time (ms)",
    min_value=0,
    max_value=60000,
    value=1200,
    step=50,
    key="workflow_response"
)

workflow_logs = st.text_area(
    "Workflow System Logs",
    value=(
        "ERROR Database connection failed\n"
        "CRITICAL Server response timeout"
    ),
    height=130,
    key="workflow_logs"
)

if st.button("Run Multi-Agent Investigation"):
    try:
        report = investigate_system(
            workflow_cpu,
            workflow_response,
            workflow_logs
        )

       
        st.subheader("Investigation Summary")

        status = report["status"].lower()

        if "normal" in status and "issue" not in status:
            st.success(f"System Status: {report['status']}")
        elif "anomaly" in status or "issue" in status:
            st.warning(f"System Status: {report['status']}")
        else:
            st.info(f"System Status: {report['status']}")

        st.markdown("### 🔍 Probable Root Cause")
        st.info(report["probable_cause"])

        col1, col2, col3 = st.columns(3)

        col1.metric("CPU Usage", f"{workflow_cpu:.1f}%")
        col2.metric("Response Time", f"{workflow_response} ms")
        col3.metric(
            "Log Lines",
            len([line for line in workflow_logs.splitlines() if line.strip()])
        )


        st.subheader("Evidence")
        for item in report["evidence"]:
            st.write("•", item)

        st.subheader("Related Knowledge")
        if report["knowledge"]:
            for i, item in enumerate(
                report["knowledge"], start=1
            ):
                with st.expander(
                    f"Result {i}: {item['topic']}"
                ):
                    st.caption(
                        f"Relevance score: {item['score']}"
                    )
                    st.text(item["content"])
        else:
            st.info("No relevant knowledge found.")

        st.subheader("Prioritized Recommendations")
        for i, item in enumerate(
            report["recommendations"], start=1
        ):
            st.markdown(
                f"**{i}. {item['priority']} Priority — "
                f"{item['action']}**"
            )
            st.write(item["details"])
            
        # Generate a report from the actual investigation
        report_text = generate_report(report)

        st.download_button(
            label="📥 Download Investigation Report",
            data=report_text,
            file_name="TraceBack_AI_Investigation_Report.txt",
            mime="text/plain",
        )


    except Exception as error:
        st.error(
            f"Multi-agent investigation failed: {error}"
        )
