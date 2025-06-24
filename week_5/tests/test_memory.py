import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from memory import get_context, update, clear

def test_memory_roundtrip():
    clear()
    update("What is IAM?", "IAM is Identity and Access Management.")
    update("How do I create a user?", "Use aws iam create-user.")
    
    context = get_context()
    assert "What is IAM?" in context
    assert "create a user" in context
