# src/bedrock_client.py

import boto3
import json
from dotenv import load_dotenv
import os

load_dotenv()

try:
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
except Exception as e:
    bedrock = None
    print(f"[ERROR] Failed to initialize Bedrock client: {e}")

def invoke_claude(messages: list, model_id="arn:aws:bedrock:us-east-2:255327957065:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0") -> str:
    if not bedrock:
        return "[ERROR] Bedrock client not initialized."

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7
    }

    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body)
        )

        result = json.loads(response["body"].read())
        return result["content"][0]["text"].strip()

    except Exception as e:
        return f"[ERROR] Claude invocation failed: {e}"
