import ray
import sys
import os

# Ensure the project root is in PYTHONPATH
sys.path.append(os.getcwd())

from actors.coding_actor import CodingActor
from core.workspace import GlobalWorkspace
from core.scheduler import Scheduler
from core.model_registry import ModelRegistry

def test_coding_actor():
    ray.init(ignore_reinit_error=True)

    workspace = GlobalWorkspace.remote()
    scheduler = Scheduler.remote()
    model_id = "Apriel-1.6-15B-Thinker"
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

    ray.shutdown()

if __name__ == "__main__":
    test_coding_actor()
