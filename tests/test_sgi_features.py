import unittest
from core.workspace import GlobalWorkspace
from core.drives import DriveEngine, calculate_entropy
from core.heartbeat import CognitiveHeartbeat
from memory.memory_manager import MemoryManager, calculate_information_density
from actors.search_actor import SearchActor
from actors.reasoner_actor import ReasonerActor

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
        memory_manager = MemoryManager()
        heartbeat = CognitiveHeartbeat(workspace, scheduler, dps, memory_manager=memory_manager)

        # Low entropy case (empty history defaults to 1.0, but let's force it)
        workspace.history = [{"type": "msg1"}] * 10
        heartbeat.heartbeat_tick() # Should be low entropy -> consolidate

        # High entropy case
        workspace.history = [{"type": f"msg{i}"} for i in range(100)]
        heartbeat.heartbeat_tick() # Should be high entropy -> replan

    def test_license_guardian(self):
        workspace = GlobalWorkspace()
        scheduler = MockScheduler()
        search_actor = SearchActor(workspace, scheduler)

        search_actor.receive({"type": "search_request", "data": "test query"})
        # scheduler should have search_result
        priority, module, message = scheduler.next()
        self.assertEqual(message["type"], "search_result")
        for res in message["data"]:
            self.assertNotIn("GPL", res)

    def test_information_density(self):
        text = "This is a test. This is only a test."
        density = calculate_information_density(text)
        self.assertGreater(density, 0)

if __name__ == "__main__":
    unittest.main()
