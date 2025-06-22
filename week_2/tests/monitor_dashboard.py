import streamlit as st
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh
import time
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pipeline.orchestrator import run_pipeline  

LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../pipeline.log'))

st.set_page_config(page_title="Bedrock Pipeline Monitoring", layout="wide")
st.title("Bedrock Pipeline Monitoring Dashboard")

# Sidebar controls
auto_refresh = st.sidebar.checkbox("Auto-refresh", value=True)
refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 2, 30, 5)

# Helper to parse logs into a DataFrame
def parse_logs(log_file):
    if not os.path.exists(log_file):
        return pd.DataFrame(columns=["Timestamp", "Level", "Message"])
    rows = []
    with open(log_file) as f:
        for line in f:
            if line.startswith("["):
                try:
                    level, rest = line[1:].split(" ", 1)
                    timestamp, msg = rest.split("] ", 1)
                    rows.append({
                        "Timestamp": timestamp.strip(),
                        "Level": level.strip(),
                        "Message": msg.strip()
                    })
                except Exception:
                    continue
    return pd.DataFrame(rows)

# Main dashboard logic
def dashboard():
    # Manual pipeline trigger button
    st.subheader("Manual Pipeline Trigger")
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if st.button("Run Pipeline Now"):
        with st.spinner("Running pipeline..."):
            try:
                response = run_pipeline("Tell me a joke")
                st.success(f"Pipeline ran successfully:")
                st.info(response)
                # Save to session history
                st.session_state['history'].append({
                    'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'response': response
                })
            except Exception as e:
                st.error(f"Pipeline error: {e}")
                st.session_state['history'].append({
                    'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'response': f"ERROR: {e}"
                })

    # Show manual run history
    if st.session_state['history']:
        st.subheader("Manual Run History (This Session)")
        hist_df = pd.DataFrame(st.session_state['history'])
        st.dataframe(hist_df.iloc[::-1], use_container_width=True)

    log_df = parse_logs(LOG_FILE)
    if log_df.empty:
        st.warning("No logs found. Run the pipeline to generate logs.")
        return

    # Enhanced summary metrics
    st.subheader("Summary Metrics")
    total_requests = len(log_df[log_df['Message'].str.contains('Received prompt')])
    successes = (log_df['Level'] == 'SUCCESS').sum()
    errors = (log_df['Level'] == 'ERROR').sum()
    last_success = log_df[log_df['Level']=='SUCCESS']['Timestamp'].max() if not log_df[log_df['Level']=='SUCCESS'].empty else 'N/A'
    last_error = log_df[log_df['Level']=='ERROR']['Timestamp'].max() if not log_df[log_df['Level']=='ERROR'].empty else 'N/A'
    avg_response_len = int(log_df[log_df['Message'].str.contains('Response:')]['Message'].str.len().mean() or 0)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Requests", total_requests)
    col2.metric("Successes", successes)
    col3.metric("Errors", errors)
    col4.metric("Last Success", last_success)
    col5.metric("Last Error", last_error)
    st.caption(f"Average Response Length: {avg_response_len} characters")

    # Show recent logs
    st.subheader("Recent Logs")
    st.dataframe(log_df.tail(30).iloc[::-1], use_container_width=True)

    # Filter logs by level
    st.subheader("Log Level Filter")
    level = st.selectbox("Select log level", ["ALL"] + sorted(log_df['Level'].unique()))
    if level != "ALL":
        st.dataframe(log_df[log_df['Level'] == level].tail(100).iloc[::-1], use_container_width=True)

    # Error details
    st.subheader("Error Details")
    error_logs = log_df[log_df['Level'] == 'ERROR']
    if not error_logs.empty:
        st.write(error_logs[['Timestamp', 'Message']].tail(10))
    else:
        st.success("No errors detected!")

# Use st_autorefresh for auto-refresh
if auto_refresh:
    st_autorefresh(interval=refresh_interval * 1000, key="dashboard_autorefresh")
dashboard()
