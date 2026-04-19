import ray
import heapq

@ray.remote
class Scheduler:
    def __init__(self):
        self.queue = []
        self._counter = 0

    def submit(self, module, message, priority=1.0):
        # Use counter as a tie-breaker to avoid comparing modules
        # module can be a Ray ActorHandle
        heapq.heappush(self.queue, (-priority, self._counter, module, message))
        self._counter += 1

    def next(self):
        if not self.queue:
            return None
        neg_priority, count, module, message = heapq.heappop(self.queue)
        return (-neg_priority, module, message)
