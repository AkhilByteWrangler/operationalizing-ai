# Amazon Q CLI - Intelligent AWS Assistant

A terminal-based conversational assistant that answers AWS-related questions step-by-step using Amazon Bedrock and Claude. This tool behaves like a smarter AWS CLI helper with memory, caching, and interactive or one-liner support.

---

## Features

- Step-by-step guidance on AWS CLI, services, errors, and setup
- Persistent conversation memory (via `diskcache`)
- Interactive REPL and one-liner CLI support
- Focused only on AWS-related content (just like Amazon Q)
- Built with `Click`, `Rich`, `diskcache`, and Bedrock integration

---

## Setup

### 1. Clone the project

```bash
git clone
cd amazon-q-cli
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure AWS credentials

Make sure your environment has access to Bedrock with Claude:

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1
```

Optionally, use a `.env` file with `python-dotenv`.

---

## Usage

### Start interactive CLI

```bash
python cli.py or just q 
```

### Ask one-liner questions

```bash
python cli.py "how do I set up an EC2 instance?" or q "How do I login into AWS thorugh CLI?"
```

### Clear memory

```bash
python cli.py clear or q clear
```

### Install Globally

To run `q` from anywhere:

```bash
chmod +x cli.py
sudo ln -s $(realpath cli.py) /usr/local/bin/q
```

---

## Example

```bash
python cli.py "how do I deploy a Lambda function with environment variables?"
q "how do I deploy a Lambda function with environment variables?"
```

**Q:**

1. Create a deployment package...
2. Use this CLI command:
   aws lambda create-function ...
3. Add env vars:
   aws lambda update-function-configuration --environment ...

Done!

---

## Guardrails

Claude responses are strictly scoped to AWS topics. Memory ensures relevant previous steps are reused, making it ideal for debugging and walkthroughs.

---

## Project Structure

```
.
├── cli.py            # Entry point
├── q_engine.py       # Prompt builder and Bedrock interface
├── memory.py         # Persistent memory using diskcache
├── requirements.txt
└── ...
```

---

## Deliverables

- Working CLI assistant
- Memory and caching tests
- User documentation (this file)

## Built with 💙 using:

- Amazon Bedrock
- Anthropic Claude
- Click
- Rich
- diskcache

---

## Testing

To run the test suite and verify CLI, memory, and engine functionality:

python-m pytest

---



## Example output

```
============================================================================= test session starts ==============================================================================
platform darwin -- Python 3.13.0, pytest-8.4.1, pluggy-1.6.0
rootdir: /Users/akhilchintalapati/Documents/Operationalizing-AI/operationalizing-ai/week_5
collected 4 items

tests/test_cli.py ..
tests/test_memory.py .
tests/test_q_engine.py .

============================================================================ 4 passed in 10.75s ==============================================================================
```

- Tests cover CLI invocation, memory clearing, and Q engine logic.
- All tests should pass if your environment and AWS credentials are set up correctly.

---
