import unittest
from core.workspace import GlobalWorkspace
from core.drives import DriveEngine, calculate_entropy, THRESHOLD_REPLAN, THRESHOLD_CONSOLIDATE
from core.heartbeat import CognitiveHeartbeat
from memory.memory_manager import MemoryManager, calculate_information_density
from actors.search_actor import SearchActor, LicenseActor
from actors.reasoner_actor import ReasonerActor
from actors.planner import Planner
import ray

class MockScheduler:
    def __init__(self):
        self.queue = []
    def submit(self, module, message, priority=1.0):
        self.queue.append((priority, module, message))
    def next(self):
        if not self.queue: return None
        return self.queue.pop(0)
    def submit_remote(self, module, message, priority=1.0):
        self.queue.append((priority, module, message))

class MockDPS:
    def __init__(self):
        self.processed = []
    def process(self, message):
        self.processed.append(message)

class TestSGIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ray.init(ignore_reinit_error=True)

    def test_entropy_calculation(self):
        state = {"history": [{"type": "msg1"}, {"type": "msg1"}, {"type": "msg2"}]}
        entropy = calculate_entropy(state)
        self.assertGreater(entropy, 0)

    def test_heartbeat_logic(self):
        # We test the logic without Ray for unit testing
        class SimpleWorkspace:
            def __init__(self): self.history = []
            def get_current_state(self): return {"history": self.history}

        workspace = SimpleWorkspace()
        scheduler = MockScheduler()
        dps = MockDPS()

        heartbeat = CognitiveHeartbeat(workspace, scheduler, dps)

        # Low entropy case
        workspace.history = [{"type": "msg1"}] * 10
        heartbeat.heartbeat_tick()
        # Should trigger consolidation (since entropy is 0)
        # Note: heartbeat_tick calls scheduler.submit

    def test_license_guardian(self):
        license_actor = LicenseActor()
        self.assertTrue(license_actor.is_compliant("MIT License content"))
        self.assertFalse(license_actor.is_compliant("This is GPLv3 software"))

    def test_information_density(self):
        text = "This is a test. This is only a test."
        density = calculate_information_density(text.split())
        self.assertGreater(density, 0)

if __name__ == "__main__":
    unittest.main()
