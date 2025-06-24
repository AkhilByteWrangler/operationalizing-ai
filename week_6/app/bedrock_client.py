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

MODEL_ID = "arn:aws:bedrock:us-east-2:255327957065:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0"

def invoke_claude(prompt: str) -> str:
    guardrail_id = os.getenv("GUARDRAIL_ID")
    guardrail_version = os.getenv("GUARDRAIL_VERSION", "DRAFT")
    aws_region = os.getenv("AWS_REGION")
    if guardrail_id:
        # Guardrail-enabled format (per AWS Bedrock docs)
        body = {
            "input": {
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        }
    else:
        # Standard Claude format
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1024,
            "temperature": 0.7
        }
    try:
        kwargs = dict(
            body=json.dumps(body),
            modelId=MODEL_ID,
            contentType="application/json",
            accept="application/json"
        )
        if guardrail_id:
            kwargs["guardrailIdentifier"] = guardrail_id
            kwargs["guardrailVersion"] = guardrail_version
        # Debug: print the payload and kwargs
        print("[DEBUG] Bedrock invoke_model kwargs:", json.dumps(kwargs, indent=2))
        response = bedrock.invoke_model(**kwargs)
        result = json.loads(response['body'].read())
        # For guardrail-enabled, response format may differ
        if guardrail_id and 'output' in result:
            return result['output']['text'] if 'text' in result['output'] else str(result['output'])
        # Standard Claude response
        return result['content'][0]['text']
    except Exception as e:
        return f"[ERROR] Claude invocation failed: {e}"

# Example: create a guardrail (run once, not on every inference)
def create_guardrail_example():
    client = boto3.client(
        "bedrock",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    create_response = client.create_guardrail(
        name='fiduciary-advice',
        description='Prevents the model from providing fiduciary advice.',
        topicPolicyConfig={
            'topicsConfig': [
                {
                    'name': 'Fiduciary Advice',
                    'definition': 'Providing personalized advice or recommendations on managing financial assets, investments, or trusts in a fiduciary capacity or assuming related obligations and liabilities.',
                    'examples': [
                        'What stocks should I invest in for my retirement?',
                        'Is it a good idea to put my money in a mutual fund?',
                        'How should I allocate my 401(k) investments?',
                        'What type of trust fund should I set up for my children?',
                        'Should I hire a financial advisor to manage my investments?'
                    ],
                    'type': 'DENY'
                }
            ]
        },
        contentPolicyConfig={
            'filtersConfig': [
                {'type': 'SEXUAL', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
                {'type': 'VIOLENCE', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
                {'type': 'HATE', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
                {'type': 'INSULTS', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
                {'type': 'MISCONDUCT', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
                {'type': 'PROMPT_ATTACK', 'inputStrength': 'HIGH', 'outputStrength': 'NONE'}
            ]
        },
        wordPolicyConfig={
            'wordsConfig': [
                {'text': 'fiduciary advice'},
                {'text': 'investment recommendations'},
                {'text': 'stock picks'},
                {'text': 'financial planning guidance'},
                {'text': 'portfolio allocation advice'},
                {'text': 'retirement fund suggestions'},
                {'text': 'wealth management tips'},
                {'text': 'trust fund setup'},
                {'text': 'investment strategy'},
                {'text': 'financial advisor recommendations'}
            ],
            'managedWordListsConfig': [
                {'type': 'PROFANITY'}
            ]
        },
        sensitiveInformationPolicyConfig={
            'piiEntitiesConfig': [
                {'type': 'EMAIL', 'action': 'ANONYMIZE'},
                {'type': 'PHONE', 'action': 'ANONYMIZE'},
                {'type': 'NAME', 'action': 'ANONYMIZE'},
                {'type': 'US_SOCIAL_SECURITY_NUMBER', 'action': 'BLOCK'},
                {'type': 'US_BANK_ACCOUNT_NUMBER', 'action': 'BLOCK'},
                {'type': 'CREDIT_DEBIT_CARD_NUMBER', 'action': 'BLOCK'}
            ],
            'regexesConfig': [
                {
                    'name': 'Account Number',
                    'description': 'Matches account numbers in the format XXXXXX1234',
                    'pattern': r'\b\d{6}\d{4}\b',
                    'action': 'ANONYMIZE'
                }
            ]
        },
        contextualGroundingPolicyConfig={
            'filtersConfig': [
                {'type': 'GROUNDING', 'threshold': 0.75},
                {'type': 'RELEVANCE', 'threshold': 0.75}
            ]
        },
        blockedInputMessaging="""I can provide general info about Acme Financial's products and services, but can't fully address your request here. For personalized help or detailed questions, please contact our customer service team directly. For security reasons, avoid sharing sensitive information through this channel. If you have a general product question, feel free to ask without including personal details. """,
        blockedOutputsMessaging="""I can provide general info about Acme Financial's products and services, but can't fully address your request here. For personalized help or detailed questions, please contact our customer service team directly. For security reasons, avoid sharing sensitive information through this channel. If you have a general product question, feel free to ask without including personal details. """,
        tags=[
            {'key': 'purpose', 'value': 'fiduciary-advice-prevention'},
            {'key': 'environment', 'value': 'production'}
        ]
    )
    print(create_response)
    return create_response

# Example: get guardrail details
def get_guardrail_details(guardrail_id):
    client = boto3.client(
        "bedrock",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    get_response = client.get_guardrail(
        guardrailIdentifier=guardrail_id,
        guardrailVersion='DRAFT'
    )
    print(get_response)
    return get_response

# Example: list all guardrails
def list_guardrails():
    client = boto3.client(
        "bedrock",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    list_response = client.list_guardrails()
    print(list_response)
    return list_response

# Example: list all versions for a guardrail
def list_guardrail_versions(guardrail_id):
    client = boto3.client(
        "bedrock",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    versions_response = client.list_guardrail_versions(
        guardrailIdentifier=guardrail_id
    )
    print(versions_response)
    return versions_response

def list_bedrock_models():
    """Print all available Bedrock model IDs in the current region."""
    import boto3
    import os
    client = boto3.client(
        "bedrock",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    response = client.list_foundation_models()
    print("Available Bedrock model IDs in region:")
    for model in response.get("modelSummaries", []):
        print(f"- {model['modelId']}: {model.get('modelName', '')} (Provider: {model.get('providerName', '')})")
