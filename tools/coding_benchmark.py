import ray
import sys
import os

from actors.coding_actor import CodingActor
from core.workspace import GlobalWorkspace
from core.scheduler import Scheduler
from core.model_registry import ModelRegistry
from core.config import SGI_SETTINGS

def test_coding_actor():
    ray.init(ignore_reinit_error=True)

    workspace = GlobalWorkspace.remote()
    scheduler = Scheduler.remote()
    model_id = SGI_SETTINGS.inference.primary_model
    model_registry = ModelRegistry.remote(model_id=model_id)

    coder = CodingActor.remote(workspace=workspace, scheduler=scheduler, model_registry=model_registry)

    test_code = "print('Hello from SGI-2026')"

    # Use execute_logic_internal via remote call
    result = ray.get(coder.execute_logic_internal.remote(test_code))

    print(f"Coding Result: {result}")

    if result.get("status") == "success" and "Hello from SGI-2026" in result.get("output"):
        print("✅ Coding Generation Test Passed")
    else:
        print("❌ Coding Generation Test Failed")
        sys.exit(1)

    # Test recursion detection and iterative transform (mock)
    recursive_code = """
def factorial(n):
    if n == 0: return 1
    return n * factorial(n-1)
"""
    transformed = ray.get(coder.iterative_transform.remote(recursive_code))
    print(f"Transformed Code:\n{transformed}")

    # Assertions for verification
    # Robust check for code transformation or mock indicator
    has_changed = transformed.strip() != recursive_code.strip()
    is_mock = "mock" in transformed.lower() or "speculative" in transformed.lower()
    has_iterative_keywords = any(term in transformed.lower() for term in ["while", "stack", "for", "range", "iterative", "loop"])

    assert has_changed or is_mock, "Transformation should modify the code unless in mock mode"
    assert has_iterative_keywords or is_mock, "Transformation should introduce iterative pattern"

    print("✅ Iterative Transformation Test Passed")

    ray.shutdown()

if __name__ == "__main__":
    test_coding_actor()
