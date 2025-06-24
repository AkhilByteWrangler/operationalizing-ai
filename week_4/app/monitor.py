from datetime import datetime

usage_metrics = []

def track_usage(endpoint: str, prompt: str):
    usage_metrics.append({
        "endpoint": endpoint,
        "prompt_length": len(prompt),
        "timestamp": datetime.now().isoformat()
    })
