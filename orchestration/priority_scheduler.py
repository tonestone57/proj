import heapq
from memory.task_graph import TaskGraph, TaskStatus

class PriorityScheduler:
    def __init__(self, task_graph: TaskGraph = None):
        self.queue = [] # Min-priority queue: (dynamic_priority, insertion_time, task, task_id)
        self.counter = 0
        self.task_graph = task_graph or TaskGraph()
        # SGI 2026: O(1) Aging Optimization.
        # Instead of decrementing all elements, we increment an offset applied to new elements.
        self.aging_offset = 0.0

    def schedule(self, task, base_priority, dependencies=None):
        # SGI 2026: Beads Integration. Add task to TaskGraph for dependency tracking.
        task_id = self.task_graph.add_task(task, dependencies, priority=base_priority)

        # Only add to active queue if it's ready
        if not dependencies:
            # Apply aging offset: new tasks enter "behind" older tasks that have aged.
            effective_priority = base_priority + self.aging_offset
            heapq.heappush(self.queue, [effective_priority, self.counter, task, task_id])
            self.counter += 1
            self.task_graph.update_task_status(task_id, TaskStatus.PENDING)

        return task_id

    def next(self, include_id=False):
        """
        Retrieves the next task.
        SGI 2026: Optimized for Intel-8265U with O(1) aging and batched unblocking.
        """
        # SGI 2026: Check TaskGraph for newly ready tasks
        ready_tasks = self.task_graph.get_ready_tasks()
        for rt in ready_tasks:
            # Check if already in queue
            if not any(item[3] == rt.task_id for item in self.queue):
                # Apply current aging offset to maintain relative priority
                effective_priority = rt.priority + self.aging_offset
                heapq.heappush(self.queue, [effective_priority, self.counter, rt.payload, rt.task_id])
                self.counter += 1
                self.task_graph.update_task_status(rt.task_id, TaskStatus.PENDING)

        if not self.queue:
            return None

        # SGI 2026: O(1) Aging.
        # Instead of O(N) iteration, we increase the offset.
        # This makes existing elements "older" (effectively lower priority value in min-heap)
        # relative to any future elements.
        self.aging_offset += 0.1

        priority, count, task, task_id = heapq.heappop(self.queue)

        # Mark as running in task graph
        self.task_graph.update_task_status(task_id, TaskStatus.RUNNING)

        if include_id:
            return task, task_id
        return task

    def clear(self):
        self.queue = []
        self.counter = 0
        self.aging_offset = 0.0
