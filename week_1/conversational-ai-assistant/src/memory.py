# src/memory.py

class Memory:
    def __init__(self, max_turns=3):
        self.history = []
        self.max_turns = max_turns

    def update(self, user_input, assistant_response):
        self.history.append(("user", user_input))
        self.history.append(("assistant", assistant_response))

        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-self.max_turns * 2:]

    def get_context(self):
        return "\n\n".join([
            f"{'Human' if role == 'user' else 'Assistant'}: {content}"
            for role, content in self.history
        ])

    def get_messages(self, user_input=None):
        # Returns the conversation as a list of Claude chat messages
        messages = [
            {"role": role, "content": content}
            for role, content in self.history
        ]
        if user_input is not None:
            messages.append({"role": "user", "content": user_input})
        return messages
