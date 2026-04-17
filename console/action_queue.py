Implements safe queuing of agent actions awaiting human approval.
Microsoft Community
class ActionQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, action):
        self.queue.append(action)

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        return None