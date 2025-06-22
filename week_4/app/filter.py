def is_safe(prompt: str) -> bool:
    banned = ["violence", "hate", "self-harm"]
    return not any(word in prompt.lower() for word in banned)
