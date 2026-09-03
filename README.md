# 🤖 Autonomous Local EDA & Insights Agent

An autonomous data analytics agent engineered with **LangGraph**, **Llama 3 (via Ollama)**, and **Streamlit**.

The agent accepts arbitrary tabular CSV datasets, automatically inspects schema distributions, dynamically generates and executes Python Seaborn/Matplotlib visualization scripts, self-heals syntax errors via a cyclical state graph, and produces structured executive business summaries.

---

## 🏗️ System Architecture

Unlike simple LLM prompting wrappers, this system operates as a deterministic, stateful graph:

```text
[Raw CSV Upload]
       │
       ▼
[Schema Profiling Node] ────► Evaluates dimensions, datatypes, missingness
       │
       ▼
[Plan & Code Node] ─────────► Llama 3 writes statistical plotting script
       │
       ▼
[Execution Sandbox] ────────► Executes Python locally & saves PNG artifacts
       │
       ├─► (On Traceback Error) ──► Loops back to LLM with stack trace
       │
       ▼ (On Successful Run)
[Synthesis Node] ───────────► Generates Executive Business Report

✨ Key Features
Schema Discovery: Automatically inspects column distributions, memory footprint, data types, and missing value densities.

Dynamic Visualizations: Generates targeted distribution histograms, correlation heatmaps, and category breakdowns using Matplotlib and Seaborn.

Cyclical Self-Healing: Catches runtime tracebacks in generated Python code and feeds errors back into Llama 3 to refactor and re-execute automatically.

Complete Data Privacy: Runs 100% locally via Ollama with open-weight models; no proprietary data or tokens are transmitted to external third-party cloud APIs.

Executive Summaries: Translates descriptive statistics into business anomalies and 3 testable strategic hypotheses.

🛠️ Tech Stack
Agent Orchestration: LangGraph, LangChain

Local LLM Runtime: Meta Llama 3 (8B) via Ollama

Data & Computation: Pandas, NumPy

Visual Analytics: Seaborn, Matplotlib

Interface: Streamlit

📁 Repository Structure
Plaintext
├── app.py                      # Streamlit frontend dashboard
├── workflow.py                 # LangGraph state machine & conditional retry routing
├── core_nodes.py               # Profiling, code generation, exec sandbox, and synthesis
├── agent_state.py              # TypedDict schema defining the agent graph state
├── transactions_sample.csv     # Lightweight sample dataset for quick testing
├── sample_insights_report.md   # Example output synthesized by the agent
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
🚀 Quickstart: Run Locally
1. Prerequisites
Install Ollama on your machine and pull the Llama 3 model:

Bash
ollama pull llama3:8b
Ensure Ollama is running in the background.

2. Clone Repository & Setup Environment
Bash
git clone git clone https://github.com/SumeetRehal/autonomous-eda-agent.git
cd autonomous-eda-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
3. Install Dependencies  
Bash
pip install -r requirements.txt
4. Launch Application
Bash
streamlit run app.py
Open http://localhost:8501 in your browser, upload transactions_sample.csv, and click Run Autonomous Analysis.

🛡️ Data Privacy & Safety Considerations
Data Residency: All data processing and LLM inferences remain strictly on local compute, making it compliant for sensitive or regulated datasets.
