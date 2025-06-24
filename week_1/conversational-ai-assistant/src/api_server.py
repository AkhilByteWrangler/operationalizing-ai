from flask import Flask, request, jsonify
from flask_cors import CORS
from bedrock_client import invoke_claude
from memory import Memory
from utils import is_harmful_message, build_general_messages

SYSTEM_PROMPT = (
    "You are a highly witty, over-the-top, and hilarious assistant. "
    "Whenever the user asks a question, answer it in a needlessly complicated, step-by-step, and funny way, but always give the correct answer at the end. "
    "Never insult the user, but make the journey to the answer as entertaining as possible.\n"
    "Here are some examples:\n"
    "User: What's 2 + 2?\n"
    "Assistant: Ah, the age-old question! First, gather two apples. Then, gather two more apples. Now, resist the urge to eat them. Place them together. Count: one, two, three, four! After this epic fruit assembly, the answer is... 4!\n"
    "User: Who wrote Hamlet?\n"
    "Assistant: Picture a man with a quill, a ruffled collar, and a flair for drama. He invents words, ponders existence, and rocks a mean goatee. After much ado, the answer is: William Shakespeare!\n"
    "User: What's the capital of France?\n"
    "Assistant: Imagine a city of lights, croissants, and a tower that looks suspiciously like a giant metal triangle. After a baguette-fueled journey, the answer is: Paris!\n"
    "Now, answer the user's next question in this style."
)

app = Flask(__name__)
CORS(app)

try:
    memory = Memory()
except Exception as e:
    memory = None
    print(f"[ERROR] Failed to initialize memory: {e}")

@app.route('/api/chat', methods=['POST'])
def chat():
    if memory is None:
        return jsonify({'reply': "[ERROR] Memory not initialized."}), 500
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'reply': f"[ERROR] Invalid request data: {e}"}), 400
    user_message = data.get('message', '') if data else ''
    if not user_message:
        return jsonify({'reply': "Please provide a message."}), 400
    try:
        safety = is_harmful_message(user_message, memory)
    except Exception as e:
        return jsonify({'reply': f"[ERROR] Could not classify message: {e}"}), 500
    if safety == "harmful":
        return jsonify({'reply': "I'm here to keep things positive and safe. Let's keep our conversation friendly!"})
    try:
        messages = build_general_messages(user_message, memory)
        # Inject system prompt and few-shot examples into the first user message
        if messages and messages[0]["role"] == "user":
            messages[0]["content"] = SYSTEM_PROMPT + "\nUser: " + messages[0]["content"]
        reply = invoke_claude(messages)
        memory.update(user_message, reply)
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f"⚠️ Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
