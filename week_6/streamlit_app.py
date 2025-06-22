import streamlit as st
import requests
import os
from datetime import datetime

# --- Config ---
API_URL = os.getenv("FASTAPI_URL", "http://localhost:8000/generate")
LLM_INFO = {
    "provider": "Amazon Bedrock (Claude)",
    "region": os.getenv("AWS_REGION", "us-east-2"),
    "model": os.getenv("MODEL_ID", "anthropic.claude-3-5-haiku-20241022-v1:0"),
    "guardrails": os.getenv("GUARDRAIL_ID", "(none)") != "(none)",
}
API_HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": os.getenv("API_KEY", "your_api_key"),
    "X-User": "streamlit-user"
}

SHORT_INPUTS = {"hi", "hello", "hey", "thanks", "thank you"}

def generate_prompt(user_input: str) -> str:
    user_input_clean = user_input.lower().strip()
    short_inputs = {
        "hi", "hello", "hey", "thanks", "thank you", 
        "what can you do", "who are you", "help", "what is this"
    }

    if user_input_clean in short_inputs or len(user_input_clean.split()) < 4:
        # Casual prompt: ask Claude to respond or clarify
        return (
            "You are a helpful AI assistant. If the user input is unclear, nonsensical, or too short, respond politely and ask for clarification.\n"
            f"User input: {user_input}\n"
            "Assistant:"
        )

    # For normal questions: request reasoning transparency
    return (
        "You are a responsible AI assistant. When answering the user, explain your reasoning clearly so they understand how you arrived at the answer.\n"
        f"User question: {user_input}\n"
        "Assistant response with reasoning:"
    )


# --- Page Setup ---
st.set_page_config(page_title="Responsible AI Chatbot", page_icon="🤖")
st.title("🤖 Responsible AI Chatbot")

# --- Sidebar Settings ---
with st.sidebar:
    st.header("⚙️ Settings")
    show_markdown = st.checkbox("Render markdown in responses", value=True)
    debug_mode = st.checkbox("Show LLM payload details", value=False)
    if st.button("🗑️ Clear All Chat & Logs"):
        st.session_state.clear()
        st.success("Session cleared!")

# --- Info Box ---
with st.expander("ℹ️ Responsible AI Info", expanded=True):
    st.markdown(f"""
    **Provider:** `{LLM_INFO['provider']}`  
    **Model:** `{LLM_INFO['model']}`  
    **Region:** `{LLM_INFO['region']}`  
    ---
    - Your chat stays in the browser.
    - No server-side logging or training.
    - Chain-of-thought reasoning is used where appropriate.
    """)

# --- Session State Defaults ---
st.session_state.setdefault("chat", [])
st.session_state.setdefault("history", [])
st.session_state.setdefault("logs", [])

# --- Message Container ---
chat_box = st.container()

# --- Input Handling ---
if prompt := st.chat_input("Ask your question here..."):
    with st.spinner("Thinking..."):
        cot_prompt = generate_prompt(prompt)
        payload = {"prompt": cot_prompt, "history": st.session_state.history.copy()}

        try:
            response = requests.post(API_URL, json=payload, headers=API_HEADERS, timeout=60)
            response.raise_for_status()
            data = response.json()

            if data.get("blocked"):
                reason = data.get("reason", "Request blocked.")
                model_steps = ["👮 Prompt blocked: " + reason] if prompt.lower().strip() not in SHORT_INPUTS else [
                    "Hi! 👋 I'm ready to help with questions that need step-by-step thinking."]
                model_reply = None
            else:
                model_reply = data.get("result", "")
                model_steps = [s.strip() for s in model_reply.split(". ") if s.strip()]
                st.session_state.history.extend([
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": model_reply}
                ])

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.chat.append((prompt, model_steps, timestamp))
            st.session_state.logs.append({
                "prompt": prompt,
                "cot_prompt": cot_prompt,
                "model_reply": model_reply,
                "timestamp": timestamp,
                "blocked": data.get("blocked", False),
                "llm_info": data.get("llm_info", {}),
                "final_llm_payload": data.get("final_llm_payload", {})
            })

        except requests.exceptions.RequestException as e:
            st.session_state.chat.append((prompt, [f"🚨 API error: {e}"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        except Exception as e:
            st.session_state.chat.append((prompt, [f"⚠️ Unexpected error: {e}"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

# --- Display Chat ---
with chat_box:
    for user_msg, model_steps, timestamp in st.session_state.chat:
        with st.chat_message("user"):
            st.markdown(user_msg)
        with st.chat_message("assistant"):
            st.markdown(f"🕓 *{timestamp}*")
            if model_steps:
                st.markdown("**Chain of Thought:**" if len(model_steps) > 1 else "**Response:**")
                for step in model_steps:
                    st.markdown(f"- {step}" if show_markdown else step)
            else:
                st.info("🤖 No response returned.")

# --- Debug Output (Optional) ---
if debug_mode and st.session_state.logs:
    with st.expander("🔍 LLM Payload & Info", expanded=False):
        st.json(st.session_state.logs[-1])  # Show last request
