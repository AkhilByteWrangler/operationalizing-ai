# pipeline/orchestrator.py
from pipeline.bedrock_client import invoke_claude
from pipeline.logger import log
import time
from functools import wraps

# Retry decorator
def retry_on_failure(max_retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    log.error(f"Attempt {attempts} failed: {e}")
                    if attempts < max_retries:
                        log.info(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        log.error("Max retries reached. Failing workflow.")
                        raise
        return wrapper
    return decorator

@retry_on_failure(max_retries=3, delay=2)
def run_pipeline(prompt: str):
    log.info(f"Received prompt: {prompt}")

    messages = [{"role": "user", "content": prompt}]
    response = invoke_claude(messages)
    if response.startswith("[ERROR]"):
        log.error(response)
        raise Exception(response)

    log.success("Claude responded successfully")
    log.info(f"Response: {response}")

    return response
