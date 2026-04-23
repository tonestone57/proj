
class EventRouter:
    def __init__(self):
        self.subscribers = {} # event_type -> list of subscribers
        self.global_listeners = []

    def subscribe(self, agent, event_type=None):
        if event_type:
            self.subscribers.setdefault(event_type, []).append(agent)
        else:
            self.global_listeners.append(agent)

    def route(self, event):
        # SGI 2026: Multi-cast event routing with filtering
        e_type = event.get("type", "generic")
        targets = self.subscribers.get(e_type, []) + self.global_listeners

        delivered_count = 0
        for agent in targets:
            # Check if agent has a filter method
            if hasattr(agent, "event_filter") and not agent.event_filter(event):
                continue

            if hasattr(agent, "receive"):
                agent.receive(event)
            elif hasattr(agent, "handle"):
                agent.handle(event)
            delivered_count += 1

        return delivered_count
