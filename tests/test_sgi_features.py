import unittest
import ray
import asyncio
from core.workspace import GlobalWorkspace
from core.scheduler import Scheduler
from core.drives import calculate_entropy
from memory.memory_manager import MemoryManager, calculate_information_density
from actors.search_actor import SearchActor

class TestSGIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ray.init(ignore_reinit_error=True, num_cpus=2)

    @classmethod
    def tearDownClass(cls):
        ray.shutdown()

    def test_entropy_calculation(self):
        state = {"history": [{"type": "msg1"}, {"type": "msg1"}, {"type": "msg2"}]}
        entropy = calculate_entropy(state)
        self.assertGreater(entropy, 0)

        state_uniform = {"history": [{"type": "msg1"}, {"type": "msg2"}]}
        entropy_uniform = calculate_entropy(state_uniform)
        self.assertEqual(entropy_uniform, 1.0)

    def test_ray_core_infrastructure(self):
        workspace = GlobalWorkspace.remote()
        scheduler = Scheduler.remote()

        workspace.broadcast.remote({"type": "test_msg"})
        state = ray.get(workspace.get_current_state.remote())
        self.assertEqual(state["current_broadcast"]["type"], "test_msg")

    def test_license_guardian(self):
        workspace = GlobalWorkspace.remote()
        scheduler = Scheduler.remote()
        # SGI 2026: License Guardian test with improved polling
        search_actor = SearchActor.remote(workspace, scheduler)

        search_actor.receive.remote({"type": "search_request", "data": "test query"})

        # Poll scheduler for results
        found = False
        # Increase timeout/retries for distributed execution
        for _ in range(30):
            res = ray.get(scheduler.next.remote())
            if res:
                priority, actor, message = res
                if message["type"] == "search_result":
                    found = True
                    # Verification: Ensure no GPL content leaked through
                    for r in message["data"]:
                        self.assertNotIn("GPL", str(r).upper())
                    break
            import time
            time.sleep(0.2)

        self.assertTrue(found, "Search results not received within timeout")

    def test_information_density(self):
        text = "This is a test. This is only a test."
        density = calculate_information_density(text.split())
        self.assertGreater(density, 0)

if __name__ == "__main__":
    unittest.main()
