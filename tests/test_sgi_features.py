import unittest
from core.workspace import GlobalWorkspace
from core.drives import DriveEngine, calculate_entropy, THRESHOLD_REPLAN, THRESHOLD_CONSOLIDATE
from core.heartbeat import CognitiveHeartbeat
from memory.memory_manager import MemoryManager, calculate_information_density
from actors.search_actor import SearchActor
from actors.reasoner_actor import ReasonerActor
from actors.planner import Planner

class MockScheduler:
    def __init__(self):
        self.queue = []
    def submit(self, module, message, priority=1.0):
        self.queue.append((priority, module, message))
    def next(self):
        if not self.queue: return None
        return self.queue.pop(0)

class MockDPS:
    def __init__(self):
        self.processed = []
    def process(self, message):
        self.processed.append(message)

class TestSGIIntegration(unittest.TestCase):
    def test_entropy_calculation(self):
        state = {"history": [{"type": "msg1"}, {"type": "msg1"}, {"type": "msg2"}]}
        entropy = calculate_entropy(state)
        self.assertGreater(entropy, 0)

        state_uniform = {"history": [{"type": "msg1"}, {"type": "msg2"}]}
        entropy_uniform = calculate_entropy(state_uniform)
        self.assertEqual(entropy_uniform, 1.0)

    def test_heartbeat_logic(self):
        workspace = GlobalWorkspace()
        scheduler = MockScheduler()
        dps = MockDPS()
        memory_manager = MemoryManager(workspace, scheduler)
        planner = Planner(workspace, scheduler)
        heartbeat = CognitiveHeartbeat(workspace, scheduler, dps, planner=planner, memory_manager=memory_manager)

        # Low entropy case
        workspace.history = [{"type": "msg1"}] * 10
        heartbeat.heartbeat_tick()

        entropy = calculate_entropy(workspace.get_current_state())

        # Check scheduler
        if entropy < THRESHOLD_CONSOLIDATE:
            task = scheduler.next()
            self.assertIsNotNone(task, "Expected a task in scheduler for low entropy")
            priority, module, message = task
            self.assertEqual(message["type"], "trigger_sleep_cycle")
            self.assertEqual(module, memory_manager)

        # High entropy case
        workspace.history = [{"type": f"msg{i}"} for i in range(100)]
        heartbeat.heartbeat_tick()

        entropy = calculate_entropy(workspace.get_current_state())

        if entropy > THRESHOLD_REPLAN:
            task = scheduler.next()
            self.assertIsNotNone(task, "Expected a task in scheduler for high entropy")
            priority, module, message = task
            self.assertEqual(message["type"], "goal")
            self.assertEqual(module, planner)

    def test_license_guardian(self):
        workspace = GlobalWorkspace()
        scheduler = MockScheduler()
        search_actor = SearchActor(workspace, scheduler)

        search_actor.receive({"type": "search_request", "data": "test query"})
        # scheduler should have search_result
        task = scheduler.next()
        self.assertIsNotNone(task)
        priority, module, message = task
        self.assertEqual(message["type"], "search_result")
        for res in message["data"]:
            self.assertNotIn("GPL", res)

    def test_information_density(self):
        text = "This is a test. This is only a test."
        density = calculate_information_density(text.split())
        self.assertGreater(density, 0)

if __name__ == "__main__":
    unittest.main()
