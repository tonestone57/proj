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

def test_task_dependency_enforcement_with_priority(clean_db):
    tg = TaskGraph(db_path=clean_db)
    scheduler = PriorityScheduler(task_graph=tg)

    # Task A: no dependencies
    task_a_id = scheduler.schedule({"name": "Task A"}, 1.0)

    # Task B: depends on Task A, high priority (low number)
    scheduler.schedule({"name": "Task B"}, 0.5, dependencies=[task_a_id])

    # Task C: no dependencies, medium priority
    scheduler.schedule({"name": "Task C"}, 0.8)

    # scheduler.next() should return Task C (0.8 < 1.0)
    task = scheduler.next()
    assert task["name"] == "Task C"

    task = scheduler.next()
    assert task["name"] == "Task A"

    # Complete Task A
    tg.update_task_status(task_a_id, TaskStatus.COMPLETED)

    # Now Task B should be ready with priority 0.5
    task = scheduler.next()
    assert task["name"] == "Task B"

def test_persistence_with_priority(clean_db):
    tg = TaskGraph(db_path=clean_db)
    tid = tg.add_task({"name": "Persistent Task"}, priority=4.2)

    # Create a new TaskGraph instance pointing to the same DB
    tg2 = TaskGraph(db_path=clean_db)
    node = tg2.get_task(tid)

    assert node is not None
    assert node.priority == 4.2
