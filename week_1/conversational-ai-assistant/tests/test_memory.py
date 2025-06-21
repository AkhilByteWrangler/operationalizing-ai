import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from memory import Memory

def test_memory_updates_and_context():
    m = Memory()

    # Check initial context is empty
    assert m.get_context() == ""

    # Add one interaction
    m.update("Hello", "Hi!")
    context = m.get_context()
    assert "Human: Hello" in context
    assert "Assistant: Hi!" in context

    # Add more interactions to test history trimming
    for i in range(4):
        m.update(f"Question {i}", f"Answer {i}")

    # Update context after all updates
    context = m.get_context()
    # Should only keep last 3 interactions (6 lines)
    context_lines = context.split("\n\n")
    assert len(context_lines) <= 6
    assert "Question 3" in context
