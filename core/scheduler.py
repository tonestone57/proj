import heapq
import ray

@ray.remote
class Scheduler:
    def __init__(self):
        self.queue = []
        self._counter = 0

    def submit(self, module_handle, message, priority=1.0):
        # Store module handle for remote execution later
        heapq.heappush(self.queue, (-priority, self._counter, module_handle, message))
        self._counter += 1

    def next(self):
        if not self.queue:
            return None
        neg_priority, count, module_handle, message = heapq.heappop(self.queue)
        return (-neg_priority, module_handle, message)
