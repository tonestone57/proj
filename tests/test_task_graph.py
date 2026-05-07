import pytest
import os
import shutil
import ray
from memory.task_graph import TaskGraph, TaskStatus
from core.scheduler import Scheduler

@pytest.fixture(scope="module")
def ray_init():
    ray.init(ignore_reinit_error=True, num_cpus=2)
    yield
    ray.shutdown()

@pytest.fixture
def clean_db():
    db_path = "./data/test_beads_db"
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
    yield db_path
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

def test_task_dependency_enforcement_with_priority(clean_db, ray_init):
    scheduler = Scheduler.remote(task_graph_db_path=clean_db)

    # Task A: no dependencies, priority 1.0
    task_a_id = ray.get(scheduler.submit.remote(None, {"name": "Task A"}, 1.0))

    # Task B: depends on Task A, high priority (0.5)
    ray.get(scheduler.submit.remote(None, {"name": "Task B"}, 0.5, dependencies=[task_a_id]))

    # Task C: no dependencies, medium priority (0.8)
    ray.get(scheduler.submit.remote(None, {"name": "Task C"}, 0.8))

    # scheduler.next() should return Task C (0.8 < 1.0)
    res = ray.get(scheduler.next.remote())
    assert res is not None
    priority, module, task, tid = res
    assert task["name"] == "Task C"

    # Next should be Task A (1.0)
    res = ray.get(scheduler.next.remote())
    assert res is not None
    priority, module, task, tid = res
    assert task["name"] == "Task A"

    # scheduler.next() should be None as Task B is blocked
    res = ray.get(scheduler.next.remote())
    assert res is None

    # Complete Task A
    ray.get(scheduler.complete_task.remote(task_a_id))

    # Now Task B should be ready and returned
    res = ray.get(scheduler.next.remote())
    assert res is not None
    priority, module, task, tid = res
    assert task["name"] == "Task B"

def test_persistence_with_priority(clean_db):
    tg = TaskGraph(db_path=clean_db)
    tid = tg.add_task({"name": "Persistent Task"}, priority=4.2)

    # Create a new TaskGraph instance pointing to the same DB
    tg2 = TaskGraph(db_path=clean_db)
    node = tg2.get_task(tid)

    assert node is not None
    assert node.priority == 4.2
