import os
import re
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from langchain_ollama import ChatOllama
from agent_state import EDAState

llm = ChatOllama(model="llama3:8b", temperature=0)

def profile_schema(state: EDAState) -> dict:
    df = state["df"]
    buffer = [f"Dataset Dimensions: {df.shape[0]} rows, {df.shape[1]} columns\n"]
    buffer.append("Columns, Data Types, and Missing Count:")
    for col in df.columns:
        buffer.append(f"- {col} (dtype: {df[col].dtype}): {df[col].isnull().sum()} missing")
    return {"schema_summary": "\n".join(buffer)}

def plan_and_generate_code(state: EDAState) -> dict:
    error_context = ""
    if state.get("execution_error"):
        error_context = f"\nPREVIOUS ERROR TO FIX:\n{state['execution_error']}\nFix the issue and return clean code."

    prompt = f"""
    You are an autonomous Python Data Analyst.
    Dataset overview:
    {state['schema_summary']}
    {error_context}

    Write executable Python code using Matplotlib and Seaborn:
    1. Distribution histograms for all numeric variables.
    2. A correlation heatmap if >= 2 numeric columns exist.
    3. Bar charts for high-frequency categorical variables.

    STRICT RULES:
    - Assume dataframe is named `df`.
    - Save plots inside './output/' as 'plot_1.png', 'plot_2.png', etc.
    - Call plt.close('all') after each figure is saved.
    - Return ONLY the raw code inside ```python ... ``` without conversational explanations.
    """
    response = llm.invoke(prompt)
    raw_text = response.content
    match = re.search(r"```python(.*?)```", raw_text, re.DOTALL)
    code = match.group(1).strip() if match else raw_text.replace("```", "").strip()
    return {"code_to_execute": code}

def execute_code(state: EDAState) -> dict:
    os.makedirs("./output", exist_ok=True)
    for f in os.listdir("./output"):
        if f.endswith(".png"):
            os.remove(os.path.join("./output", f))
            
    local_scope = {"df": state["df"], "plt": plt, "sns": sns, "pd": pd}
    try:
        exec(state["code_to_execute"], {}, local_scope)
        return {"execution_error": None}
    except Exception as e:
        return {"execution_error": f"{type(e).__name__}: {str(e)}"}

def synthesize_insights(state: EDAState) -> dict:
    df = state["df"]
    stats = df.describe(include='all').to_string()
    prompt = f"""
    You are a Lead Data Strategist. Analyze this profile:
    Schema:
    {state['schema_summary']}
    Summary Statistics:
    {stats}
    
    Write an executive markdown report covering:
    - Data Health & Anomaly Check
    - Key Analytical Observations
    - 3 Next-Step Hypotheses
    """
    response = llm.invoke(prompt)
    return {"insights_report": response.content}
