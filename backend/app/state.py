class ConversationState:

    def __init__(self):
        self.state = "guide"

    def update(self, mode):
        self.state = mode

    def current(self):
        return self.state