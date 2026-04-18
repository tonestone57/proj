LinkedIn
class EventRouter:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, agent):
        self.subscribers.setdefault(event_type, []).append(agent)

    def route(self, event):
        for agent in self.subscribers.get(event["type"], []):
            agent.handle(event)
