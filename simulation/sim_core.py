
import heapq

class SimulationCore:
    def __init__(self):
        self.time = 0
        self.global_state = {}
        self.event_queue = [] # Min-priority queue based on event time

    def tick(self):
        self.time += 1
        current_events = []

        while self.event_queue and self.event_queue[0][0] <= self.time:
            time, event = heapq.heappop(self.event_queue)
            current_events.append(event)

        return current_events

    def schedule(self, event, delay=1):
        heapq.heappush(self.event_queue, (self.time + delay, event))

    def update_state(self, key, value):
        self.global_state[key] = value
