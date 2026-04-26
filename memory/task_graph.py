import lancedb
import os
import json
import uuid
import time
from typing import List, Dict, Any, Optional

class TaskStatus:
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

class TaskNode:
    def __init__(self, task_id: str, payload: Dict[str, Any], dependencies: List[str] = None, status: str = TaskStatus.PENDING, created_at: float = None):
        self.task_id = task_id
        self.payload = payload
        self.dependencies = dependencies or []
        self.status = status
        self.created_at = created_at or time.time()

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "payload": json.dumps(self.payload),
            "dependencies": json.dumps(self.dependencies),
            "status": self.status,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            task_id=data["task_id"],
            payload=json.loads(data["payload"]),
            dependencies=json.loads(data["dependencies"]),
            status=data["status"],
            created_at=data["created_at"]
        )

class TaskGraph:
    """
    SGI 2026: Beads-inspired Persistent Task Graph.
    Uses LanceDB for machine-optimized, Git-backed task persistence.
    Ensured scalability through targeted searches and proper timestamping.
    """
    def __init__(self, db_path: str = "./data/sgi_beads_db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.db = lancedb.connect(self.db_path)
        self.table_name = "task_beads"

        try:
            if self.table_name not in self.db.list_tables():
                # Schema definition for LanceDB
                self.table = self.db.create_table(self.table_name, data=[
                    {
                        "task_id": "root",
                        "payload": json.dumps({"type": "init"}),
                        "dependencies": json.dumps([]),
                        "status": TaskStatus.COMPLETED,
                        "created_at": time.time()
                    }
                ])
            else:
                self.table = self.db.open_table(self.table_name)
        except (ValueError, RuntimeError) as e:
            # Handle potential race condition or existing table
            self.table = self.db.open_table(self.table_name)

    def add_task(self, payload: Dict[str, Any], dependencies: List[str] = None) -> str:
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        status = TaskStatus.READY if not dependencies else TaskStatus.BLOCKED
        node = TaskNode(task_id, payload, dependencies, status)

        self.table.add([node.to_dict()])
        return task_id

    def get_task(self, task_id: str) -> Optional[TaskNode]:
        res = self.table.search().where(f"task_id = '{task_id}'").to_list()
        if res:
            return TaskNode.from_dict(res[0])
        return None

    def update_task_status(self, task_id: str, status: str):
        node = self.get_task(task_id)
        if node:
            self.table.update(where=f"task_id = '{task_id}'", values={"status": status})

            if status == TaskStatus.COMPLETED:
                self._unblock_dependents(task_id)

    def _unblock_dependents(self, completed_task_id: str):
        # Optimization: Search only for tasks that are currently BLOCKED
        blocked_tasks = self.table.search().where(f"status = '{TaskStatus.BLOCKED}'").to_list()
        for task_data in blocked_tasks:
            deps = json.loads(task_data["dependencies"])
            if completed_task_id in deps:
                # Check if all dependencies are now met
                if self._check_dependencies_met(deps):
                    self.update_task_status(task_data["task_id"], TaskStatus.READY)

    def _check_dependencies_met(self, dependencies: List[str]) -> bool:
        # Optimization: Check if all dependencies are in COMPLETED status
        for dep_id in dependencies:
            dep_node = self.get_task(dep_id)
            if not dep_node or dep_node.status != TaskStatus.COMPLETED:
                return False
        return True

    def get_ready_tasks(self) -> List[TaskNode]:
        res = self.table.search().where(f"status = '{TaskStatus.READY}'").to_list()
        return [TaskNode.from_dict(t) for t in res]
