import unittest
import sys
import os
import ray

# Add the repo root to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from actors.coding_actor import CodingActor

class MockModelRegistry:
    def __init__(self, response):
        self.response = response
    def generate(self, prompt, **kwargs):
        return self.response
    def receive(self, message): return False

@ray.remote
class MockModelRegistryActor:
    def __init__(self, response):
        self.response = response
    def generate(self, prompt, **kwargs):
        return self.response
    def receive(self, message): return False

class TestCodingActorRobustness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ray.init(ignore_reinit_error=True, num_cpus=1)

    @classmethod
    def tearDownClass(cls):
        ray.shutdown()

    def test_iterative_transform_fallback(self):
        # Mock LLM returning invalid python code
        mock_registry = MockModelRegistryActor.remote("This is not valid python code!")
        actor = CodingActor.remote(workspace=None, scheduler=None, model_registry=mock_registry)

        original_code = "def fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)"

        # We need to call iterative_transform. It's not a remote method in CodingActor (it inherits it)
        # But CodingActor is @ray.remote, so we use .remote()

        # However, iterative_transform is not decorated with .remote in the base class if called directly.
        # But since the class is decorated, all its methods are remote.

        # We need to find recursive funcs first or let it detect them
        transformed = ray.get(actor.iterative_transform.remote(original_code))

        # Should fallback to original code
        self.assertEqual(transformed, original_code)

if __name__ == "__main__":
    unittest.main()
