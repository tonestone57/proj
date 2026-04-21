import sys
import os
import ray

# Ensure we can import from core
sys.path.append(os.getcwd())

if not ray.is_initialized():
    ray.init(ignore_reinit_error=True)

def verify_curiosity_refinement():
    print("--- Verifying Curiosity Refinement (Saliency Pruning) ---")
    from memory.memory_manager import MemoryManager

    manager = MemoryManager.remote()

    # Initial status
    status_0 = ray.get(manager.get_status.remote())
    print(f"Initial Active Cache Size: {status_0['active_cache_size']}")
    print(f"Initial Deep Archive Size: {status_0['deep_archive_size']}")

    # Populate wisdom cache by "retrieving" some traces
    print("\nAccessing traces at Tick 10 and 100...")
    ray.get(manager.retrieve_wisdom_traces.remote("AVX2", current_tick=10))
    ray.get(manager.retrieve_wisdom_traces.remote("thermal", current_tick=100))
    # 'quantiz' is never accessed (last_tick = 0)

    # Trigger sleep cycle at tick 150
    # AVX2: 150-10 = 140 (OK)
    # thermal: 150-100 = 50 (OK)
    # quantiz: 150-0 = 150 (OK)
    print("\nTriggering sleep cycle at Tick 150...")
    ray.get(manager.trigger_sleep_cycle.remote(current_tick=150))
    status_1 = ray.get(manager.get_status.remote())
    print(f"Active Cache Size (Tick 150): {status_1['active_cache_size']}")
    assert status_1['active_cache_size'] == 3

    # Trigger sleep cycle at tick 400
    # AVX2: 400-10 = 390 (STALE)
    # thermal: 400-100 = 300 (STALE)
    # quantiz: 400-0 = 400 (STALE)
    print("\nTriggering sleep cycle at Tick 400...")
    ray.get(manager.trigger_sleep_cycle.remote(current_tick=400))
    status_2 = ray.get(manager.get_status.remote())
    print(f"Active Cache Size (Tick 400): {status_2['active_cache_size']}")
    print(f"Deep Archive Size (Tick 400): {status_2['deep_archive_size']}")

    assert status_2['active_cache_size'] == 0
    assert status_2['deep_archive_size'] == 3

    print("\n✅ Curiosity Refinement verification complete. Entries successfully moved to deep archive.")

if __name__ == "__main__":
    verify_curiosity_refinement()
    ray.shutdown()
