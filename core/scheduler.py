import ray
import heapq
import logging
from memory.task_graph import TaskGraph, TaskStatus
from core.config import SCHEDULER_AGING_INC

# SGI 2026: Distributed Ray-based Scheduler
logger = logging.getLogger(__name__)

@ray.remote
class Scheduler:
    """
    SGI 2026: Distributed Ray-based Scheduler.
    Integrates persistent TaskGraph for dependency tracking and implements O(1) aging.

    Note: self.task_modules stores ephemeral Ray ActorHandles.
    On scheduler restart, persistent tasks in TaskGraph may lose their target module handles.
    Future recovery should utilize a global ActorRegistry to re-bind handles by name/type.
    """
    def __init__(self, task_graph_db_path: str = "./data/sgi_beads_db"):
        self.queue = [] # Min-priority queue: [effective_priority, counter, module, message, task_id]
        self._counter = 0
        self.task_graph = TaskGraph(db_path=task_graph_db_path)
        # SGI 2026: O(1) Aging Optimization using integer offset to prevent float drift.
        self.aging_offset = 0
        # Map task_id to module because Ray handles aren't JSON serializable for TaskGraph persistence
        self.task_modules = {}
        # O(1) set for tracking IDs currently in the queue
        self.queued_task_ids = set()

    def submit(self, module, message, priority=1.0, dependencies=None):
        # SGI 2026: Beads Integration. Add task to TaskGraph for dependency tracking.
        task_id = self.task_graph.add_task(message, dependencies, priority=priority)
        self.task_modules[task_id] = module

        # Only add to active queue if it's ready
        if not dependencies:
            self._push_to_queue(module, message, priority, task_id)

        return task_id

    def _push_to_queue(self, module, message, priority, task_id):
        # SGI 2026: Lower numerical value = Higher priority.
        # Apply aging offset: new tasks enter "behind" older tasks that have aged.
        effective_priority = priority + self.aging_offset
        heapq.heappush(self.queue, [effective_priority, self._counter, module, message, task_id])
        self.queued_task_ids.add(task_id)
        self._counter += 1
        # Use ready status for the queue to distinguish from blocked
        self.task_graph.update_task_status(task_id, TaskStatus.PENDING)

    def next(self):
        """
        Retrieves the next task.
        SGI 2026: Optimized for Intel-8265U with O(1) aging and batched unblocking.
        """
        # SGI 2026: Check TaskGraph for newly ready tasks
        ready_tasks = self.task_graph.get_ready_tasks()

        for rt in ready_tasks:
            # Check if already in queue (O(1) lookup)
            if rt.task_id not in self.queued_task_ids:
                module = self.task_modules.get(rt.task_id)

                # SGI 2026: Resilience - Don't queue tasks with lost handles unless they are handle-less
                # (e.g. system-level broadcasts).
                # Note: Test tasks often use None as module, so we allow it if payload is simple.
                if module is None and rt.payload and isinstance(rt.payload, dict) and rt.payload.get("target_required", True):
                    # We check if it's a real system task or just a test/dummy task
                    if rt.payload.get("type"):
                         logger.error(f"Handle lost for task {rt.task_id} ({rt.payload.get('type')}). Skipping to prevent crash.")
                         self.task_graph.update_task_status(rt.task_id, TaskStatus.FAILED)
                         continue

                self._push_to_queue(module, rt.payload, rt.priority, rt.task_id)

        if not self.queue:
            return None

        # SGI 2026: O(1) Aging. Increment offset to age all existing tasks.
        self.aging_offset += SCHEDULER_AGING_INC

        eff_priority, count, module, message, task_id = heapq.heappop(self.queue)
        self.queued_task_ids.remove(task_id)

        # Mark as running in task graph
        self.task_graph.update_task_status(task_id, TaskStatus.RUNNING)

        return (eff_priority - self.aging_offset, module, message, task_id)

    def complete_task(self, task_id):
        """Marks a task as completed and cleanup modules."""
        self.task_graph.update_task_status(task_id, TaskStatus.COMPLETED)
        if task_id in self.task_modules:
            del self.task_modules[task_id]
