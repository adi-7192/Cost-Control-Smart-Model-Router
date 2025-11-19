import streamlit as st
import pandas as pd
import requests
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import RequestLog
from app.config import settings

# Setup DB connection
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

st.set_page_config(page_title="Cost-Control Router Dashboard", layout="wide")

st.title("🚀 Cost-Control Smart Model Router")
st.markdown("Enter a prompt below to see how it gets routed to different models based on difficulty.")

# Sidebar for Config
st.sidebar.header("Configuration")
current_classifier = settings.CLASSIFIER_TYPE
st.sidebar.info(f"Current Classifier: **{current_classifier}**")
st.sidebar.markdown("To change classifier, update `.env` or environment variables and restart.")

# --- Interactive Section ---
st.subheader("Try it out!")
with st.form("prompt_form"):
    prompt_input = st.text_area("Enter your prompt:", height=100, placeholder="e.g., What is 2+2? or Write a Python script to...")
    submitted = st.form_submit_button("Route Prompt")

if submitted and prompt_input:
    try:
        # Call the API
        api_url = "http://127.0.0.1:8000/route"
        with st.spinner("Routing and processing..."):
            response = requests.post(api_url, json={"prompt": prompt_input})
            
        if response.status_code == 200:
            result = response.json()
            
            # Display Result
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Difficulty", result["difficulty"].upper())
            col2.metric("Model Selected", result["model"])
            col3.metric("Cost", f"${result['cost']:.6f}")
            col4.metric("Latency", f"{result['latency_ms']:.2f} ms")
            
            st.info(f"**Reasoning:** {result['reasoning']}")
            st.success(f"Response: {result['response']}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            st.warning("Make sure the backend server is running: `uvicorn app.main:app --reload`")
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to backend server.")
        st.info("Please run the backend server in a separate terminal: `uvicorn app.main:app --reload`")

st.divider()

# --- Analytics Section ---
# Auto-refresh logic
if st.sidebar.checkbox("Auto-refresh Logs (5s)", value=True):
    time.sleep(5)
    st.rerun()

def get_data():
    db = SessionLocal()
    logs = db.query(RequestLog).order_by(RequestLog.timestamp.desc()).limit(50).all()
    db.close()
    return logs

logs = get_data()

if not logs:
    st.info("No requests logged yet.")
else:
    data = []
    for log in logs:
        data.append({
            "ID": log.id,
            "Time": log.timestamp.strftime("%H:%M:%S"),
            "Prompt": log.prompt_preview,
            "Difficulty": log.difficulty,
            "Reasoning": log.reasoning,
            "Model": log.model_used,
            "Cost ($)": log.cost,
            "Tokens": log.tokens_used,
            "Latency (ms)": f"{log.response_time_ms:.2f}"
        })
    
    df = pd.DataFrame(data)
    
    st.subheader("Recent Routing Logs")
    
    # Metrics
    total_cost = df["Cost ($)"].sum()
    total_requests = len(df)
    
    m1, m2 = st.columns(2)
    m1.metric("Total Cost (Last 50)", f"${total_cost:.6f}")
    m2.metric("Total Requests", total_requests)

    # Table
    st.dataframe(df, use_container_width=True)
    
    # Charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.caption("Model Distribution")
        model_counts = df["Model"].value_counts()
        st.bar_chart(model_counts)
        
    with col_right:
        st.caption("Difficulty Distribution")
        diff_counts = df["Difficulty"].value_counts()
        st.bar_chart(diff_counts)
