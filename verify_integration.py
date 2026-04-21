import sys
import os
import ray

# Ensure we can import from core
sys.path.append(os.getcwd())

if not ray.is_initialized():
    ray.init(ignore_reinit_error=True)

def verify_distillation_integration():
    print("--- Verifying Integrated Structural Distillation ---")
    from memory.memory_manager import MemoryManager

    manager = MemoryManager.remote()

    # We need to make sure the chunks are identical after comment removal
    code = """def test_func():
    # comment 1
    return "Hello"

def test_func():
    # comment 2
    return "Hello"
"""

    result = ray.get(manager.perform_structural_distillation.remote(code))
    print("Distillation Result:")
    print(f"'{result}'")

    # Should have no comments and the second function should be hashed
    assert "#" not in result
    assert "[HASH:" in result

    print("\n✅ Integrated Distillation verification complete.")

if __name__ == "__main__":
    verify_distillation_integration()
    ray.shutdown()
