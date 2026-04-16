Allows modules to communicate safely.
class EventBus:
    def __init__(self):
        self.queue = []

    def publish(self, event):
        self.queue.append(event)

    def consume(self):
        if self.queue:
            return self.queue.pop(0)
        return None