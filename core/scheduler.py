import ray
import heapq
from memory.task_graph import TaskGraph, TaskStatus

@ray.remote
class Scheduler:
    def __init__(self, task_graph_db_path: str = "./data/sgi_beads_db"):
        self.queue = [] # Min-priority queue: [effective_priority, counter, module, message, task_id]
        self._counter = 0
        self.task_graph = TaskGraph(db_path=task_graph_db_path)
        # SGI 2026: O(1) Aging Optimization.
        self.aging_offset = 0.0
        # Map task_id to module because Ray handles aren't JSON serializable for TaskGraph persistence
        self.task_modules = {}

    def submit(self, module, message, priority=1.0, dependencies=None):
        # SGI 2026: Beads Integration. Add task to TaskGraph for dependency tracking.
        task_id = self.task_graph.add_task(message, dependencies, priority=priority)
        self.task_modules[task_id] = module

        # Only add to active queue if it's ready
        if not dependencies:
            # SGI 2026: Lower numerical value = Higher priority.
            # Apply aging offset: new tasks enter "behind" older tasks that have aged.
            effective_priority = priority + self.aging_offset
            heapq.heappush(self.queue, [effective_priority, self._counter, module, message, task_id])
            self._counter += 1
            self.task_graph.update_task_status(task_id, TaskStatus.PENDING)

        return task_id

    def next(self):
        """
        Retrieves the next task.
        SGI 2026: Optimized for Intel-8265U with O(1) aging and batched unblocking.
        """
        # SGI 2026: Check TaskGraph for newly ready tasks
        ready_tasks = self.task_graph.get_ready_tasks()

        # Optimization: Use a set for O(1) lookup of task IDs currently in queue
        current_queued_ids = {item[4] for item in self.queue}

        for rt in ready_tasks:
            # Check if already in queue
            if rt.task_id not in current_queued_ids:
                module = self.task_modules.get(rt.task_id)
                message = rt.payload

                # Apply current aging offset to maintain relative priority
                effective_priority = rt.priority + self.aging_offset
                heapq.heappush(self.queue, [effective_priority, self._counter, module, message, rt.task_id])
                self._counter += 1
                self.task_graph.update_task_status(rt.task_id, TaskStatus.PENDING)

        if not self.queue:
            return None

        # SGI 2026: O(1) Aging.
        self.aging_offset += 0.1

        eff_priority, count, module, message, task_id = heapq.heappop(self.queue)

        # Mark as running in task graph
        self.task_graph.update_task_status(task_id, TaskStatus.RUNNING)

        # Return original priority (approximated from effective) or message priority
        return (eff_priority - self.aging_offset, module, message)

    def complete_task(self, task_id):
        """Marks a task as completed and cleanup modules."""
        self.task_graph.update_task_status(task_id, TaskStatus.COMPLETED)
        if task_id in self.task_modules:
            del self.task_modules[task_id]
