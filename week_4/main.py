from fastapi import FastAPI, Request
from bedrock_client import invoke_claude
import logging
from datetime import datetime

app = FastAPI()

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    if not prompt:
        return {"error": "No prompt provided"}

    logging.info(f"[{datetime.now()}] Prompt: {prompt}")
    response = invoke_claude(prompt)
    return {"response": response}
