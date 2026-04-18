class GlobalWorkspace:
    def __init__(self):
        self.subscribers = []
        self.current_broadcast = None

    def register(self, module):
        self.subscribers.append(module)

    def broadcast(self, message):
        self.current_broadcast = message
        for module in self.subscribers:
            module.receive(message)
