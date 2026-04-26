import heapq
from memory.task_graph import TaskGraph, TaskStatus

class PriorityScheduler:
    def __init__(self, task_graph: TaskGraph = None):
        self.queue = [] # Min-priority queue: (dynamic_priority, insertion_time, task, task_id)
        self.counter = 0
        self.task_graph = task_graph or TaskGraph()

    def schedule(self, task, base_priority, dependencies=None):
        # SGI 2026: Beads Integration. Add task to TaskGraph for dependency tracking.
        task_id = self.task_graph.add_task(task, dependencies)

        # Only add to active queue if it's ready
        if not dependencies:
            heapq.heappush(self.queue, [base_priority, self.counter, task, task_id])
            self.counter += 1

    def next(self, include_id=False):
        """
        Retrieves the next task.
        SGI 2026: Backward compatible. Returns task by default, or (task, task_id) if include_id is True.
        """
        # SGI 2026: Check TaskGraph for newly ready tasks
        ready_tasks = self.task_graph.get_ready_tasks()
        for rt in ready_tasks:
            # Check if already in queue
            if not any(item[3] == rt.task_id for item in self.queue):
                # Add to queue with high priority as it was just unblocked
                heapq.heappush(self.queue, [1.0, self.counter, rt.payload, rt.task_id])
                self.counter += 1
                # Mark as pending so we don't pick it up again from get_ready_tasks
                self.task_graph.update_task_status(rt.task_id, TaskStatus.PENDING)

        if not self.queue:
            return None

        # Task Aging
        for item in self.queue:
            item[0] -= 0.1

        heapq.heapify(self.queue)
        priority, count, task, task_id = heapq.heappop(self.queue)

        # Mark as running in task graph
        self.task_graph.update_task_status(task_id, TaskStatus.RUNNING)

        if include_id:
            return task, task_id
        return task

    def clear(self):
        self.queue = []
        self.counter = 0
