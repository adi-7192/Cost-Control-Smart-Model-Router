import streamlit as st
import pandas as pd
import requests
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import RequestLog
from app.config import settings

# Page config
st.set_page_config(
    page_title="Cost-Control Router",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .response-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    /* Fix metric cards - force dark background with white text */
    [data-testid="stMetric"] {
        background-color: #1e1e1e !important;
        padding: 1rem !important;
        border-radius: 0.5rem !important;
        border: 1px solid #333 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    /* Fix text colors for dark theme */
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: inherit !important;
    }
    .stMarkdown h2 {
        color: #ffffff !important;
    }
    .stMarkdown h3 {
        color: #e0e0e0 !important;
    }
    /* Ensure markdown text is visible */
    [data-testid="stMarkdownContainer"] {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Setup DB connection
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sidebar - Settings
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.title("⚙️ Settings")
    
    # API Keys Section
    with st.expander("🔑 API Configuration", expanded=False):
        st.markdown("**Add your API keys to enable real LLM routing**")
        
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Enter your OpenAI API key for GPT-4o"
        )
        
        google_key = st.text_input(
            "Google API Key",
            type="password",
            placeholder="AIza...",
            help="Enter your Google API key for Gemini"
        )
        
        if st.button("💾 Save API Keys", use_container_width=True):
            try:
                payload = {}
                if openai_key:
                    payload["OPENAI_API_KEY"] = openai_key
                if google_key:
                    payload["GOOGLE_API_KEY"] = google_key
                
                if payload:
                    response = requests.post("http://127.0.0.1:8000/config/keys", json=payload)
                    if response.status_code == 200:
                        st.success("✅ API keys saved successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Failed to save keys")
                else:
                    st.warning("Please enter at least one API key")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.divider()
    
    # System Info
    st.markdown("**System Status**")
    current_classifier = settings.CLASSIFIER_TYPE
    st.info(f"🧠 Classifier: **{current_classifier.upper()}**")
    
    # Auto-refresh
    auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=False)
    if auto_refresh:
        time.sleep(5)
        st.rerun()
    
    st.divider()
    st.caption("Made with ❤️ using Streamlit")

# Main Content
st.markdown('<h1 class="main-header">🚀 Cost-Control Smart Model Router</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Intelligent LLM routing that reduces costs by up to 70% through smart model selection</p>', unsafe_allow_html=True)

# Prompt Input Section
st.subheader("💬 Try it Out")

col1, col2 = st.columns([3, 1])
with col1:
    prompt_input = st.text_area(
        "Enter your prompt:",
        height=120,
        placeholder="e.g., 'What is 2+2?' or 'Explain quantum physics in detail'",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.button("🚀 Send", use_container_width=True, type="primary")
    
    if st.button("🗑️ Clear", use_container_width=True):
        st.rerun()

# Handle submission
if submit_button and prompt_input:
    try:
        api_url = "http://127.0.0.1:8000/route"
        with st.spinner("🤔 Analyzing and routing your prompt..."):
            response = requests.post(api_url, json={"prompt": prompt_input}, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # Response Display
            st.markdown('<div class="response-box">', unsafe_allow_html=True)
            st.markdown("### 📝 Response")
            st.markdown(result['response'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Metadata
            st.markdown("### 📊 Routing Details")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🎯 Difficulty", result["difficulty"].upper())
            with col2:
                st.metric("🤖 Model", result["model"])
            with col3:
                st.metric("💰 Cost", f"${result['cost']:.6f}")
            with col4:
                st.metric("⚡ Latency", f"{result['latency_ms']:.0f}ms")
            
            # Reasoning
            st.info(f"**🧠 Routing Reasoning:** {result['reasoning']}")
            
            # Cost Savings Comparison
            st.markdown("### 💰 Cost Savings Analysis")
            
            savings = result.get('savings', 0)
            cost_without = result.get('cost_without_routing', 0)
            savings_pct = result.get('savings_percentage', 0)
            
            # Create comparison card
            if savings > 0:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 20px; border-radius: 10px; color: white; margin: 10px 0;">
                    <h4 style="color: white; margin: 0 0 15px 0;">💚 Smart Routing Savings</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                            <div style="font-size: 0.9em; opacity: 0.9;">Smart Routing</div>
                            <div style="font-size: 1.5em; font-weight: bold;">${result['cost']:.6f}</div>
                            <div style="font-size: 0.8em; opacity: 0.8;">✓ {result['model']}</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                            <div style="font-size: 0.9em; opacity: 0.9;">Without Routing</div>
                            <div style="font-size: 1.5em; font-weight: bold;">${cost_without:.6f}</div>
                            <div style="font-size: 0.8em; opacity: 0.8;">✗ GPT-4o only</div>
                        </div>
                        <div style="background: rgba(76, 175, 80, 0.3); padding: 15px; border-radius: 8px; border: 2px solid #4CAF50;">
                            <div style="font-size: 0.9em; opacity: 0.9;">You Saved</div>
                            <div style="font-size: 1.5em; font-weight: bold;">${savings:.6f}</div>
                            <div style="font-size: 0.8em; opacity: 0.8;">🎉 {savings_pct:.1f}% cheaper!</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Calculate projections for 1000 requests/day
                daily_savings = savings * 1000
                monthly_savings = daily_savings * 30
                yearly_savings = daily_savings * 365
                
                # Show projection
                st.markdown(f"""
                <div style="background: rgba(76, 175, 80, 0.1); border-left: 4px solid #4CAF50; 
                            padding: 15px; border-radius: 5px; margin: 10px 0;">
                    <h4 style="margin: 0 0 10px 0;">📊 The Big Picture: Scale Projection</h4>
                    <p style="margin: 5px 0; font-size: 0.95em;">
                        <strong>If you made 1,000 requests like this every day:</strong>
                    </p>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 15px;">
                        <div>
                            <div style="font-size: 0.85em; opacity: 0.8;">Daily Savings</div>
                            <div style="font-size: 1.3em; font-weight: bold; color: #4CAF50;">${daily_savings:.2f}</div>
                        </div>
                        <div>
                            <div style="font-size: 0.85em; opacity: 0.8;">Monthly Savings</div>
                            <div style="font-size: 1.3em; font-weight: bold; color: #4CAF50;">${monthly_savings:.2f}</div>
                        </div>
                        <div>
                            <div style="font-size: 0.85em; opacity: 0.8;">Yearly Savings</div>
                            <div style="font-size: 1.3em; font-weight: bold; color: #4CAF50;">${yearly_savings:,.2f}</div>
                        </div>
                    </div>
                    <p style="margin: 15px 0 0 0; font-size: 0.9em; opacity: 0.9;">
                        💡 <em>At scale, smart routing could save you <strong>${yearly_savings:,.2f}/year</strong> compared to using GPT-4o for everything!</em>
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("💡 This query used the most powerful model (GPT-4o) for best quality.")
            
        else:
            st.error(f"❌ Error: {response.status_code} - {response.text}")
            st.warning("Make sure the backend server is running: `uvicorn app.main:app --reload`")
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to backend server")
        st.info("💡 Start the server: `uvicorn app.main:app --reload`")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

st.divider()

# Analytics Section
st.markdown('''
<div style="background-color: #000000; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
    <h2 style="color: #ffffff; margin: 0;">📈 Analytics & Recent Activity</h2>
</div>
''', unsafe_allow_html=True)

# Fetch data
def get_data():
    db = SessionLocal()
    logs = db.query(RequestLog).order_by(RequestLog.timestamp.desc()).limit(100).all()
    db.close()
    return logs

logs = get_data()

if not logs:
    st.info("📭 No requests logged yet. Try submitting a prompt above!")
else:
    # Prepare data
    data = []
    for log in logs:
        data.append({
            "Time": log.timestamp.strftime("%H:%M:%S"),
            "Prompt": log.prompt_preview,
            "Difficulty": log.difficulty,
            "Model": log.model_used,
            "Cost ($)": log.cost,
            "Tokens": log.tokens_used,
            "Latency (ms)": round(log.response_time_ms, 2)
        })
    
    df = pd.DataFrame(data)
    
    # Calculate cumulative savings
    # Estimate what GPT-4o would have cost for all requests
    total_tokens = df['Tokens'].sum()
    gpt4o_total_cost = (total_tokens / 1000) * 0.03
    actual_total_cost = df['Cost ($)'].sum()
    total_savings = gpt4o_total_cost - actual_total_cost
    savings_pct = (total_savings / gpt4o_total_cost * 100) if gpt4o_total_cost > 0 else 0
    
    # Summary Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📊 Total Requests", len(df))
    with col2:
        st.metric("💵 Actual Cost", f"${actual_total_cost:.6f}")
    with col3:
        st.metric("💰 Without Routing", f"${gpt4o_total_cost:.6f}", 
                 delta=f"-${total_savings:.6f}", delta_color="inverse")
    with col4:
        st.metric("💚 Total Saved", f"${total_savings:.6f}",
                 delta=f"{savings_pct:.1f}%", delta_color="normal")
    with col5:
        avg_latency = df['Latency (ms)'].mean()
        st.metric("⚡ Avg Latency", f"{avg_latency:.0f}ms")
    
    # Charts - Horizontal and Smaller
    st.markdown('''
    <div style="background-color: #000000; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <h3 style="color: #ffffff; margin: 0;">📊 Distribution Charts</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Model Usage Chart
    st.markdown('''
    <div style="background-color: #000000; padding: 8px; border-radius: 5px; margin: 10px 0;">
        <p style="color: #ffffff; margin: 0;"><strong>Model Usage</strong></p>
    </div>
    ''', unsafe_allow_html=True)
    model_counts = df["Model"].value_counts()
    model_chart_df = pd.DataFrame({
        'Model': model_counts.index,
        'Count': model_counts.values
    })
    
    import altair as alt
    model_chart = alt.Chart(model_chart_df).mark_bar().encode(
        x=alt.X('Count:Q', title='Number of Requests'),
        y=alt.Y('Model:N', title='Model', sort='-x'),
        color=alt.value('#667eea')
    ).properties(height=150)
    st.altair_chart(model_chart, use_container_width=True)
    
    # Difficulty Breakdown Chart  
    st.markdown('''
    <div style="background-color: #000000; padding: 8px; border-radius: 5px; margin: 10px 0;">
        <p style="color: #ffffff; margin: 0;"><strong>Difficulty Breakdown</strong></p>
    </div>
    ''', unsafe_allow_html=True)
    diff_counts = df["Difficulty"].value_counts()
    diff_chart_df = pd.DataFrame({
        'Difficulty': diff_counts.index,
        'Count': diff_counts.values
    })
    
    diff_chart = alt.Chart(diff_chart_df).mark_bar().encode(
        x=alt.X('Count:Q', title='Number of Requests'),
        y=alt.Y('Difficulty:N', title='Difficulty Level', sort='-x'),
        color=alt.value('#764ba2')
    ).properties(height=150)
    st.altair_chart(diff_chart, use_container_width=True)
    
    # Recent Logs Table
    st.markdown('''
    <div style="background-color: #000000; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <h3 style="color: #ffffff; margin: 0;">📋 Recent Requests</h3>
    </div>
    ''', unsafe_allow_html=True)
    st.dataframe(
        df.head(50),
        width='stretch',
        hide_index=True
    )
