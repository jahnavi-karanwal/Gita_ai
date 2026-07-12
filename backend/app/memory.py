class ConversationMemory:

    def __init__(self, max_messages=6):
        self.max_messages = max_messages
        self.messages = []

    def add_user_message(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })
        self._trim()

    def add_assistant_message(self, message):
        self.messages.append({
            "role": "assistant",
            "content": message
        })
        self._trim()

    def get_history(self):
        return self.messages

    def clear(self):
        self.messages = []

    def _trim(self):
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]