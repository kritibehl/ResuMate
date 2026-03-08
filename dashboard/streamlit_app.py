import pandas as pd
import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8002/v1"

st.set_page_config(page_title="ResuMate Dashboard", layout="wide")
st.title("ResuMate Dashboard")

summary = requests.get(f"{BASE_URL}/dashboard/summary", timeout=5).json()
jobs = requests.get(f"{BASE_URL}/dashboard/jobs", timeout=5).json()
stability = requests.get(f"{BASE_URL}/dashboard/stability", timeout=5).json()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Jobs", summary.get("total_jobs", 0))
col2.metric("Total Batches", summary.get("total_batches", 0))
col3.metric("Avg Processing Time (ms)", summary.get("avg_processing_time_ms", 0))
col4.metric("Success Rate", f'{summary.get("success_rate", 0)}%')

st.subheader("Recent Jobs")
st.dataframe(pd.DataFrame(jobs.get("items", [])), use_container_width=True)

st.subheader("Stability")
st.dataframe(pd.DataFrame(stability.get("items", [])), use_container_width=True)
