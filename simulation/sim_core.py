api.emergentmind.com
class SimulationCore:
    def __init__(self):
        self.time = 0
        self.global_state = {}
        self.event_queue = []

    def tick(self):
        self.time += 1
        if self.event_queue:
            return self.event_queue.pop(0)
        return None

    def schedule(self, event):
        self.event_queue.append(event)
