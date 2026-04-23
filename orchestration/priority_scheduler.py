
import heapq

import heapq
import time

class PriorityScheduler:
    def __init__(self):
        self.queue = [] # Min-priority queue: (dynamic_priority, insertion_time, task)
        self.counter = 0

    def schedule(self, task, base_priority):
        # SGI 2026: Priority-based scheduling with stable insertion order
        heapq.heappush(self.queue, [base_priority, self.counter, task])
        self.counter += 1

    def next(self):
        if not self.queue:
            return None

        # Task Aging: Decrease priority value (increase importance) of all waiting tasks
        for item in self.queue:
            # SGI Starvation Prevention: slightly boost older tasks
            item[0] -= 0.1

        heapq.heapify(self.queue)
        return heapq.heappop(self.queue)[2]

    def clear(self):
        self.queue = []
