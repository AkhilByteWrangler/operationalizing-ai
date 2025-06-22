import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from q_engine import ask_q
from unittest.mock import patch

@patch("q_engine.invoke_claude")
def test_ask_q(mock_invoke):
    mock_invoke.return_value = "Here's how to launch an EC2 instance..."
    result = ask_q("How do I launch an EC2 instance?")
    assert "EC2" in result
