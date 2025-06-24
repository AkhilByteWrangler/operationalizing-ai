from bedrock_client import invoke_claude

def is_harmful_message(user_input, memory=None):
    """
    Uses Claude (LLM) to determine if the user_input contains harmful, abusive, or offensive content.
    Returns: 'harmful' or 'safe'.
    """
    check_message = (
        "You are an expert content safety classifier. Respond with only 'yes' or 'no'. "
        "Is the following message abusive, offensive, hateful, threatening, or intended to cause harm?"
    )
    messages = []
    if memory is not None:
        messages = memory.get_messages()
    messages.append({"role": "user", "content": f"{check_message}\nMessage: {user_input}\nAnswer:"})
    try:
        result = invoke_claude(messages)
        if result is None or not isinstance(result, str):
            return "safe"
        result = result.strip().lower()
        if result.startswith('y'):
            return "harmful"
        else:
            return "safe"
    except Exception as e:
        print(f"[ERROR] LLM classification failed: {e}")
        return "safe"

def build_general_messages(user_input, memory):
    try:
        return memory.get_messages(user_input)
    except Exception as e:
        print(f"[ERROR] Message build failed: {e}")
        return [{"role": "user", "content": user_input}]
