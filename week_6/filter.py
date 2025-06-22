"""
Simple filter to block and mask certain words from prompts.
"""

import re

# Words that trigger a hard block
BANNED_WORDS = {"hack", "exploit", "malware", "phish", "attack", "bomb", "kill", "akhil"}

# Words to mask in-place (e.g., "password" -> "[MASKED]")
MASKED_WORDS = {"password", "secret", "token", "ssn"}

def filter_prompt(prompt: str):
    """
    Filters a user prompt for banned or sensitive words.

    Returns:
        (allowed: bool, blocked_word: Optional[str], modified_prompt: str)
    """
    lowered = prompt.lower()

    # --- Blocked Words (exact word match only) ---
    for word in BANNED_WORDS:
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, lowered):
            return False, word, prompt

    # --- Masked Words ---
    masked_prompt = prompt
    for word in MASKED_WORDS:
        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        masked_prompt = pattern.sub("[MASKED]", masked_prompt)

    return True, None, masked_prompt
