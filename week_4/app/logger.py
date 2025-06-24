from datetime import datetime

def log_request(prompt: str):
    print(f"[{datetime.now()}] Prompt received: {prompt}")
