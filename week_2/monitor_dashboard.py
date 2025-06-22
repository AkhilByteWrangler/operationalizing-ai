import streamlit as st
import pandas as pd
import time
import os

LOG_FILE = "pipeline.log" 

st.set_page_config(page_title="Bedrock Pipeline Monitoring", layout="wide")
st.title("🛠️ Bedrock Pipeline Monitoring Dashboard")

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

# Main dashboard loop
def dashboard():
    log_df = parse_logs(LOG_FILE)
    if log_df.empty:
        st.warning("No logs found. Run the pipeline to generate logs.")
        return

    # Show summary metrics
    st.subheader("Summary Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Requests", str(len(log_df[log_df['Message'].str.contains('Received prompt')])) )
    col2.metric("Successes", str(len(log_df[log_df['Level']]=='SUCCESS')) )
    col3.metric("Errors", str(len(log_df[log_df['Level']]=='ERROR')) )

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

# Auto-refresh logic
if auto_refresh:
    while True:
        dashboard()
        time.sleep(refresh_interval)
        st.experimental_rerun()
else:
    dashboard()
