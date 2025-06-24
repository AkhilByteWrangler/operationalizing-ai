"""
FastAPI backend for Streamlit Responsible AI Chatbot 

Features:
- Exposes /generate endpoint
- Uses bedrock_client.py for LLM calls
- No server-side logging or persistent storage
- Applies banned word filters and masks sensitive terms
- Returns LLM info and responsible AI disclaimers
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.bedrock_client import invoke_claude
from filter import filter_prompt
from typing import List, Optional, Dict, Any
import os

# --- App Init ---
app = FastAPI()

# --- CORS for Streamlit frontend ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- Helper: LLM Info ---
def get_llm_info() -> Dict[str, Any]:
    return {
        "llm_provider": "Amazon Bedrock (Claude)",
        "model_id": os.getenv("MODEL_ID", "anthropic.claude-3-5-haiku-20241022-v1:0"),
        "hosted_at": f"AWS {os.getenv('AWS_REGION', 'us-east-2')} region (cloud)",
        "guardrails_enabled": bool(os.getenv("GUARDRAIL_ID")),
        "privacy_controls": "No data is stored or used for training. All logs are user-side only."
    }

# --- Helper: Sanitize Conversation History ---
def sanitize_history(history: List[Dict[str, str]]) -> List[Dict[str, str]]:
    sanitized = []
    for turn in history:
        role = turn.get("role")
        content = turn.get("content", "")
        if not content or role not in ("user", "assistant"):
            continue
        if role == "user":
            allowed, banned_word, _ = filter_prompt(content)
            if not allowed:
                raise ValueError(f"banned:{banned_word}")
            _, _, masked = filter_prompt(content)
            sanitized.append({"role": "user", "content": masked})
        else:
            sanitized.append({"role": "assistant", "content": content})
    return sanitized

# --- Endpoint: Generate ---
@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    prompt: str = data.get("prompt", "").strip()
    history: Optional[List[Dict[str, str]]] = data.get("history")
    llm_info = get_llm_info()

    if not prompt:
        return {
            "blocked": True,
            "reason": "Prompt is empty or invalid.",
            "llm_info": llm_info,
            "final_llm_payload": None
        }

    # Filter current prompt
    allowed, banned_word, _ = filter_prompt(prompt)
    if not allowed:
        return {
            "blocked": True,
            "reason": f"Your prompt contains a banned word: '{banned_word}'. Please revise your input.",
            "llm_info": llm_info,
            "final_llm_payload": None
        }

    # Mask current prompt
    _, _, masked_prompt = filter_prompt(prompt)

    try:
        if history:
            try:
                sanitized_history = sanitize_history(history)
            except ValueError as ve:
                word = str(ve).split(":")[1]
                return {
                    "blocked": True,
                    "reason": f"Your prompt history contains a banned word: '{word}'",
                    "llm_info": llm_info,
                    "final_llm_payload": None
                }
            messages = sanitized_history + [{"role": "user", "content": masked_prompt}]
            result = invoke_claude(messages)
            final_payload = {"messages": messages}
        else:
            result = invoke_claude(masked_prompt)
            final_payload = {"prompt": masked_prompt}

        # Catch blocked response from LLM
        if isinstance(result, str) and (result.startswith("[ERROR]") or "blocked" in result.lower()):
            return {
                "blocked": True,
                "reason": "Your request was blocked due to security or policy reasons.",
                "details": result,
                "llm_info": llm_info,
                "final_llm_payload": final_payload
            }

        return {
            "result": result,
            "llm_info": llm_info,
            "final_llm_payload": final_payload,
            "data_usage": "Your prompt and chat history are processed securely. No data is stored or used for training. All logs are user-side only.",
            "logs": "No server-side logs. You control your chat history."
        }

    except Exception as e:
        return {
            "blocked": True,
            "reason": "Internal error during processing.",
            "details": str(e),
            "llm_info": llm_info,
            "final_llm_payload": None
        }

# --- Health Check Endpoint ---
@app.get("/")
def root():
    return {"message": "✅ Responsible AI FastAPI backend is running."}
