import json
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Profiler graph", layout="wide")
st.title("AIPyMemTimeProfiler - Multi-Metric")

DEFAULT_PATH = Path.cwd() / "profile_output.json"

if not DEFAULT_PATH.exists():
    st.error(f"Could not find: {DEFAULT_PATH}")
    st.stop()

# Load and parse
with open(DEFAULT_PATH) as f:
    data = json.load(f)
df = pd.DataFrame(data)

st.success(f"Loaded ({len(df)} function(s))")

metrics = {
    "Execution Time (ms)": "max_time_ms",
    "CPU Time (ms)": "cpu_time_ms",
    "Peak Memory Usage (KB)": "max_mem_kb",
    "RSS Memory Growth (KB)": "mem_growth_rss_kb",
    "Return Object Size (Bytes)": "returned_size"
}

for label, key in metrics.items():
    st.markdown(f"### {label}")
    sorted_df = df.sort_values(by=key, ascending=False)

    fig = px.bar(
        sorted_df,
        x=key,
        y="function",
        orientation="h",
        color=key,
        color_continuous_scale="Reds",
        hover_data=["file", "line", "cpu_time_ms", "max_mem_kb", "mem_growth_rss_kb", "returned_size"],
        height=400 + len(sorted_df) * 20
    )

    fig.update_layout(
        xaxis_title=label,
        yaxis_title="Function",
        title=label,
        margin=dict(t=40, l=10, r=10, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)
