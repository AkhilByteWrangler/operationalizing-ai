# tests/test_pipeline.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from pipeline.orchestrator import run_pipeline
from pipeline.logger import log

# ------------- MOCKED TESTS ------------- #

@pytest.fixture
def mock_claude(mocker):
    return mocker.patch("pipeline.orchestrator.invoke_claude")

def test_pipeline_success(mock_claude, capsys):
    mock_claude.return_value = "Why did the robot go to therapy? Too many circuits to deal with!"

    prompt = "Tell me a joke"
    response = run_pipeline(prompt)

    assert isinstance(response, str)
    assert "robot" in response

    # Check logs printed
    captured = capsys.readouterr()
    assert "[SUCCESS" in captured.out
    assert "Claude responded" in captured.out

def test_pipeline_empty_response(mock_claude):
    mock_claude.return_value = ""

    response = run_pipeline("hi")
    assert response == ""

def test_pipeline_exception_handling(mock_claude):
    mock_claude.side_effect = Exception("Simulated Claude failure")

    with pytest.raises(Exception):
        run_pipeline("Trigger an error")

# ------------- OPTIONAL INTEGRATION TEST (REAL CLAUDE) -------------

def test_pipeline_real_integration():
    prompt = "Tell me a joke about computers."
    response = run_pipeline(prompt)
    assert isinstance(response, str)
    assert len(response.strip()) > 0
    assert "joke" in response.lower() or "computer" in response.lower() or "laugh" in response.lower()
