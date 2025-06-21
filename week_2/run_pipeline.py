# run_pipeline.py
from pipeline.orchestrator import run_pipeline

if __name__ == "__main__":
    while True:
        prompt = input("\nUser: ").strip()
        if prompt.lower() in ['exit', 'quit']:
            break
        result = run_pipeline(prompt)
        print(f"Assistant: {result}")
