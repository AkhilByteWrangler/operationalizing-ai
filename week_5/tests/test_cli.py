import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from click.testing import CliRunner
from cli import cli


def test_ask_q():
    runner = CliRunner()
    result = runner.invoke(cli, ['How do I create an EC2 instance?'])
    print(result.output)  
    assert result.exit_code == 0
    assert "instance" in result.output.lower()


def test_clear_memory():
    runner = CliRunner()
    result = runner.invoke(cli, ['clear'])
    print(result.output)  
    assert result.exit_code == 0
    assert ("memory cleared" in result.output.lower()) or ("amazon q is thinking" in result.output.lower())

