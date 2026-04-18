class GlobalWorkspace:
    def __init__(self):
        self.subscribers = []
        self.current_broadcast = None
        self.history = []

    def register(self, module):
        self.subscribers.append(module)

    def broadcast(self, message):
        self.current_broadcast = message
        self.history.append(message)
        # Keep history manageable
        if len(self.history) > 100:
            self.history.pop(0)

        for module in self.subscribers:
            module.receive(message)

    def get_current_state(self):
        return {
            "current_broadcast": self.current_broadcast,
            "history": self.history
        }
