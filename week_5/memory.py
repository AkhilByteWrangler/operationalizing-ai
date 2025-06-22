# memory.py
from diskcache import Cache

cache = Cache(".q_memory_cache")
HISTORY_KEY = "chat_history"
MAX_TURNS = 5

def get_context():
    """Retrieve recent Q conversation context."""
    history = cache.get(HISTORY_KEY, [])
    return "\n".join(history[-MAX_TURNS * 2:])

def update(user_input, response):
    """Add a new user-Q turn to memory."""
    history = cache.get(HISTORY_KEY, [])
    history.append(f"User: {user_input}")
    history.append(f"Q: {response}")
    cache.set(HISTORY_KEY, history)

def clear():
    cache.delete(HISTORY_KEY)
