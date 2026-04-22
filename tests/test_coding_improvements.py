import unittest
import ray
# Import CodingActorBase for direct instantiation in tests
from actors.coding_actor import CodingActorBase
from core.workspace import GlobalWorkspace
from core.scheduler import Scheduler

@ray.remote
class MockModelRegistry:
    def generate(self, prompt, **kwargs):
        # Extremely simple mock: just return a pre-canned iterative fib
        if "fib" in prompt:
            return """
def fib(n):
    if n <= 1: return n
    stack = [n]
    res = 0
    while stack:
        curr = stack.pop()
        if curr <= 1:
            res += curr
        else:
            stack.append(curr - 1)
            stack.append(curr - 2)
    return res

print(fib(5))
"""
        return "print('mock output')"

class TestCodingImprovements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Do not init ray in the test process to avoid OOM
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_recursion_detection(self):
        # Mock workspace and scheduler
        workspace = None
        scheduler = None
        # Direct instantiation of the base class
        actor = CodingActorBase(workspace, scheduler)

        code = "def f(n): return f(n-1) if n > 0 else 0"
        recursive_funcs = actor.detect_recursion(code)
        self.assertIn("f", recursive_funcs)

        code_no_rec = "def f(n): return n + 1"
        recursive_funcs_no_rec = actor.detect_recursion(code_no_rec)
        self.assertEqual(len(recursive_funcs_no_rec), 0)

    def test_iterative_transform_integration(self):
        workspace = None
        scheduler = None

        # Mock model_registry locally instead of using ray.remote
        class LocalMockModelRegistry:
            def generate(self, prompt, **kwargs):
                if "fib" in prompt:
                    return "def fib(n): return 5\nprint(fib(5))"
                return "print('mock output')"

        model_registry = LocalMockModelRegistry()
        # Direct instantiation of the base class
        actor = CodingActorBase(workspace, scheduler, model_registry=model_registry)

        code = "def fib(n): return fib(n-1) + fib(n-2) if n > 1 else n\nprint(fib(5))"
        result = actor.execute_logic_internal(code)

        self.assertEqual(result["status"], "success", f"Error: {result.get('error')}")
        self.assertIn("5", result["output"])

if __name__ == "__main__":
    unittest.main()
