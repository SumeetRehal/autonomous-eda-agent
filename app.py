import streamlit as st
import pandas as pd
import glob
from workflow import eda_graph

st.set_page_config(page_title="Colab Autonomous EDA Agent", layout="wide")
st.title("📊 Autonomous EDA & Executive Insights Agent")
st.caption("Hosted on Google Colab T4 GPU via Ollama Llama 3 & LangGraph")

uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Data Preview")
    st.dataframe(df.head(5), use_container_width=True)

    if st.button("Run Autonomous Analysis", type="primary"):
        with st.status("Agent Running Pipeline...", expanded=True):
            initial_state = {
                "df": df,
                "schema_summary": "",
                "code_to_execute": "",
                "execution_error": None,
                "insights_report": ""
            }
            result = eda_graph.invoke(initial_state)

        col1, col2 = st.columns([1.1, 0.9])
        with col1:
            st.subheader("Autonomous Visualizations")
            plots = sorted(glob.glob("./output/*.png"))
            for img in plots:
                st.image(img, use_container_width=True)
                
        with col2:
            st.subheader("Executive Insights")
            st.markdown(result["insights_report"])
            st.download_button("Download Report (.md)", result["insights_report"], "report.md")
