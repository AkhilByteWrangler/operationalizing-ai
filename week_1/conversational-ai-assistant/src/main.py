# src/main.py

from bedrock_client import invoke_claude
from memory import Memory
from utils import is_harmful_message, build_general_messages
import time
import random

GREETINGS = [
    "😂 Hey there! I'm Jokester Bot, your punny pal. Ready to laugh and learn? Ask me anything!",
    "😄 Welcome! I'm Jokester Bot, here to answer your questions—with a twist of humor!",
    "🤣 Hi! I'm Jokester Bot. Whether it's math, facts, or fun, I'll get you the answer—with a giggle!"
]

FUN_FACTS = [
    "Did you know? If you tickle a group of mathematicians, they might start giggling in sines!",
    "Why did the computer go to the doctor? Because it had a byte!",
    "Why don't skeletons fight each other? They don't have the guts!",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!"
]

HELP_TEXT = (
    "\nHow to use Jokester Bot:\n"
    "- Ask me anything—math, facts, advice, or just for a joke!\n"
    "- I’ll always answer, but expect a little humor along the way.\n"
    "- Type 'help' to see this message again.\n"
    "- Type 'exit' or 'quit' to leave.\n"
    "- Type 'fact' to hear a silly fun fact!\n"
    "- I keep things kind, positive, and fun!\n"
)

def typing_effect(text, delay=0.015):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def main():
    try:
        memory = Memory()
    except Exception as e:
        print(f"[ERROR] Failed to initialize memory: {e}")
        return

    print("\n🤖 Jokester Bot\n" + random.choice(GREETINGS))
    print("(Type 'help' for options and 'fact' for a surprise!)\n")
    turn_count = 0
    
    while True:
        try:
            user_input = input("You: ").strip()
        except Exception as e:
            print(f"[ERROR] Failed to read input: {e}")
            continue

        if user_input.lower() in ['exit', 'quit']:
            print("👋 Goodbye! Keep smiling and stay curious!")
            break

        if user_input.lower() == 'help':
            print(HELP_TEXT)
            continue

        if user_input.lower() == 'fact':
            try:
                print(random.choice(FUN_FACTS))
            except Exception as e:
                print(f"[ERROR] Could not fetch fun fact: {e}")
            continue

        if not user_input:
            print("Please enter a message or type 'help'.")
            continue

        try:
            safety = is_harmful_message(user_input, memory)
        except Exception as e:
            print(f"[ERROR] Could not classify message: {e}")
            continue

        if safety == "harmful":
            print("Assistant: I'm here to keep things positive and safe. Let's keep our conversation friendly!")
            continue

        try:
            messages = build_general_messages(user_input, memory)
            messages.append({
                "role": "system",
                "content": (
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
            })
            print("Assistant is typing...")
            response = invoke_claude(messages)
            typing_effect(f"Assistant: {response}")
            memory.update(user_input, response)
            turn_count += 1
            if turn_count == 3:
                print("(Tip: You can ask for a fun fact by typing 'fact'!)")
        except Exception as e:
            print("⚠️ Error:", e)

if __name__ == "__main__":
    main()
