import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

bedrock = boto3.client(
    "bedrock-runtime",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def invoke_claude(prompt: str) -> str:
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 800,
        "temperature": 0.7
    }

    try:
        response = bedrock.invoke_model(
            modelId="arn:aws:bedrock:us-east-2:255327957065:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0",
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )
        result = json.loads(response['body'].read())
        return result['content'][0]['text'].strip()
    except Exception as e:
        return f"[ERROR] Claude invocation failed: {e}"
