import unittest
import asyncio
from core.workspace import GlobalWorkspace
from core.drives import DriveEngine, calculate_entropy, THRESHOLD_REPLAN, THRESHOLD_CONSOLIDATE
from core.heartbeat import CognitiveHeartbeat
from memory.memory_manager import MemoryManager, calculate_information_density
from actors.search_actor import SearchActor, LicenseActor
from actors.reasoner_actor import ReasonerActor
from actors.planner import Planner
import ray

class TestSGIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ray.init(ignore_reinit_error=True, num_cpus=1)

    def test_entropy_calculation(self):
        state = {"history": [{"type": "msg1"}, {"type": "msg1"}, {"type": "msg2"}]}
        entropy = calculate_entropy(state)
        self.assertGreater(entropy, 0)

    def test_heartbeat_logic(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Use actual Ray actors for a more realistic test
        workspace = GlobalWorkspace.remote()

        class MockScheduler:
            @ray.remote
            class SchedulerActor:
                async def submit(self, *args, **kwargs): return None
            def __init__(self):
                self.actor = self.SchedulerActor.remote()
            @property
            def remote(self): return self.actor

        scheduler = MockScheduler()
        heartbeat = CognitiveHeartbeat(workspace, scheduler.actor)

        # We need to populate workspace history
        for _ in range(10):
            ray.get(workspace.broadcast.remote({"type": "msg1"}))

        # Heartbeat tick should now run without crash
        loop.run_until_complete(heartbeat.heartbeat_tick())

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
