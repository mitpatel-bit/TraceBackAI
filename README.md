# TraceBack AI — Multi-Agent Root Cause Investigator

## Project Overview
TraceBack AI is a Python-based system troubleshooting prototype that analyzes system metrics and logs to identify potential issues, retrieve relevant troubleshooting information, and recommend corrective actions.

## Features
- System anomaly detection using Isolation Forest
- Root-cause analysis using rule-based logic
- System log analysis and error classification
- TF-IDF-based troubleshooting knowledge retrieval
- Priority-based recommendations
- Interactive Streamlit dashboard
- Downloadable investigation reports

## Technologies Used
- Python
- Streamlit
- Pandas
- Scikit-learn
- TF-IDF and cosine similarity

## Project Structure
```text
TraceBackAI/
├── app.py
├── rag.py
├── root_cause_agent.py
├── recommendation_agent.py
├── multi_agent_workflow.py
├── report_generator.py
└── knowledge_base/
    └── troubleshooting.txt
```

## Installation and Usage

1. Clone or download this repository.
2. Open the project folder in VS Code.
3. Create and activate a Python virtual environment.
4. Install the required dependencies:

```bash
pip install streamlit pandas scikit-learn matplotlib
```

5. Start the dashboard:

```bash
streamlit run app.py
```

6. Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## How It Works
The system analyzes CPU usage, response time, and log messages. It identifies potential causes using predefined rules, searches a local troubleshooting knowledge base using TF-IDF similarity, and generates prioritized recommendations.

## Current Limitations
- Uses sample system metrics unless additional data sources are configured.
- Root-cause analysis relies on predefined rules.
- Knowledge retrieval uses TF-IDF rather than a generative language model.
- Diagnostic results should be verified before applying recommendations.

## Future Enhancements
- Connect to live monitoring systems.
- Expand the troubleshooting knowledge base.
- Improve diagnosis with more datasets and evaluation.
- Add optional LLM-based explanations.

## Author
Mit Prakashkumar Patel
