from fastapi import APIRouter, Request
from app.filter import is_safe
from app.logger import log_request
from app.monitor import track_usage
from bedrock_client import invoke_claude

router = APIRouter()

@router.post("/generate")
async def generate(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    if not is_safe(prompt):
        return {"error": "Unsafe or inappropriate content detected."}

    log_request(prompt)
    response = invoke_claude(prompt)
    track_usage("generate", prompt)

    return {"response": response}
