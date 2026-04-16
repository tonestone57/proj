Implements attention, priority, and competition.
class Scheduler:
    def __init__(self):
        self.queue = []

    def submit(self, module, message, priority=1.0):
        self.queue.append((priority, module, message))
        self.queue.sort(reverse=True)

    def next(self):
        if not self.queue:
            return None
        return self.queue.pop(0)