# Responsible AI Chatbot with Streamlit & FastAPI

This project demonstrates a responsible AI chatbot using Amazon Bedrock (Claude) as the LLM, with a Streamlit frontend and a FastAPI backend. It features prompt filtering, privacy controls, and responsible AI guardrails.

## Directory Structure

```
week_6/
│
├── app/
│   └── bedrock_client.py
├── filter.py
├── main.py
├── streamlit_app.py
├── .env.template
├── .env
└── venv/ (virtual environment)
```

## File Descriptions

### `app/bedrock_client.py`

- Handles all interactions with Amazon Bedrock (Claude) via the AWS SDK.
- Supports both standard and guardrail-enabled LLM calls.
- Includes helper functions for managing Bedrock guardrails and listing available models.

### `filter.py`

- Implements prompt filtering to block banned words and mask sensitive terms.
- Ensures that user prompts do not contain harmful or sensitive content before reaching the LLM.

### `main.py`

- FastAPI backend exposing a `/generate` endpoint for the chatbot.
- Applies prompt filtering and privacy controls.
- Returns LLM responses, model info, and responsible AI disclaimers.
- Includes a health check endpoint at `/`.

### `streamlit_app.py`

- Streamlit frontend for user interaction.
- Sends user prompts to the FastAPI backend and displays responses.
- Supports markdown rendering, chat history, and debug info.
- Ensures all chat data remains client-side for privacy.

### `.env.template`

- Template for environment variables required to run the backend.
- Copy to `.env` and fill in your AWS credentials and model info.

### `.env`

- **(Sensitive, do not commit!)**
  Stores actual AWS credentials and configuration for local development.

## Setup & Usage

1. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```
2. **Configure environment**

   - Copy `.env.template` to `.env` and fill in your AWS credentials and model details.
3. **Run the FastAPI backend**

   ```
   uvicorn main:app --reload
   ```
4. **Run the Streamlit frontend**

   ```
   streamlit run streamlit_app.py
   ```
5. **Open the Streamlit app**
   Visit `http://localhost:8501` in your browser.

## Responsible AI Features

- **Prompt Filtering:** Blocks and masks unsafe or sensitive content.
- **Guardrails:** Optional AWS Bedrock guardrails for additional safety.
- **Privacy:** No server-side logging or data storage; all chat history is local.
- **Transparency:** LLM info and disclaimers are shown to users.

---
