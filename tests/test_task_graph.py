import pytest
import os
import shutil
from memory.task_graph import TaskGraph, TaskStatus
from orchestration.priority_scheduler import PriorityScheduler

@pytest.fixture
def clean_db():
    db_path = "./data/test_beads_db"
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
    yield db_path
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

def test_task_dependency_enforcement(clean_db):
    tg = TaskGraph(db_path=clean_db)
    scheduler = PriorityScheduler(task_graph=tg)

    # Task A: no dependencies
    scheduler.schedule({"name": "Task A"}, 1.0)

    # Task B: depends on Task A
    ready_tasks = tg.get_ready_tasks()
    task_a_id = next(t.task_id for t in ready_tasks if t.payload["name"] == "Task A")

    scheduler.schedule({"name": "Task B"}, 2.0, dependencies=[task_a_id])

    # scheduler.next() should return Task A (legacy mode)
    task = scheduler.next()
    assert isinstance(task, dict)
    assert task["name"] == "Task A"

    # scheduler.next() should be empty now (Task B is blocked)
    assert scheduler.next() is None

    # Complete Task A
    tg.update_task_status(task_a_id, TaskStatus.COMPLETED)

    # Now Task B should be ready and returned by scheduler
    task = scheduler.next()
    assert task["name"] == "Task B"

def test_include_id_compatibility(clean_db):
    tg = TaskGraph(db_path=clean_db)
    scheduler = PriorityScheduler(task_graph=tg)
    scheduler.schedule({"name": "Task ID"}, 1.0)

    # Test new mode
    res = scheduler.next(include_id=True)
    assert isinstance(res, tuple)
    assert len(res) == 2
    task, tid = res
    assert task["name"] == "Task ID"
    assert tid.startswith("task_")

def test_persistence(clean_db):
    tg = TaskGraph(db_path=clean_db)
    tid = tg.add_task({"name": "Persistent Task"})

    # Create a new TaskGraph instance pointing to the same DB
    tg2 = TaskGraph(db_path=clean_db)
    node = tg2.get_task(tid)

    assert node is not None
    assert node.payload["name"] == "Persistent Task"
    assert node.status == TaskStatus.READY
    assert node.created_at > 0
