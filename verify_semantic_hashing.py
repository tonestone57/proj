import sys
import os
import ray

# Ensure we can import from core
sys.path.append(os.getcwd())

if not ray.is_initialized():
    ray.init(ignore_reinit_error=True)

def verify_semantic_hashing():
    print("--- Verifying Semantic Hashing ---")
    from memory.memory_manager import MemoryManager

    # Mock workspace and scheduler for MemoryManager
    manager = MemoryManager.remote()

    code_with_duplicates = """
def hello_world():
    print("Hello, world!")

def another_func():
    return 42

def hello_world():
    print("Hello, world!")
"""

    # First pass: should store hello_world
    result_1 = ray.get(manager.perform_semantic_hashing.remote(code_with_duplicates))
    print("Result 1 (First pass):")
    print(result_1)

    assert "[HASH:" in result_1
    assert result_1.count("def hello_world():") == 1
    assert "def another_func():" in result_1

    # Second pass: identical code should also be hashed if we pass it again
    code_repeated = """
def hello_world():
    print("Hello, world!")
"""
    result_2 = ray.get(manager.perform_semantic_hashing.remote(code_repeated))
    print("\nResult 2 (Repeated snippet):")
    print(result_2)
    assert "[HASH:" in result_2
    assert "def hello_world():" not in result_2

    print("\n✅ Semantic Hashing verification complete.")

if __name__ == "__main__":
    verify_semantic_hashing()
    ray.shutdown()
