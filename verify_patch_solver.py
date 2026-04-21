import sys
import os
import ray
import z3

# Ensure we can import from core
sys.path.append(os.getcwd())

if not ray.is_initialized():
    ray.init(ignore_reinit_error=True)

def verify_patch_solver():
    print("--- Verifying Z3 Config Patch Solver ---")
    from meta_learning.meta_manager import MetaManager

    manager = MetaManager.remote()

    # Test case 1: Valid patch
    valid_patch = {
        'hardware_limits': {
            'max_threads': 4,
            'thermal_threshold_celsius': 72.0,
            'low_memory_warning_mb': 2000
        }
    }
    print("\nTesting valid patch...")
    is_valid = ray.get(manager.verify_config_patch_z3.remote(valid_patch))
    assert is_valid == True, "Valid patch was incorrectly rejected"

    # Test case 2: Invalid max_threads (> 8)
    invalid_threads = {
        'hardware_limits': {
            'max_threads': 10,
            'thermal_threshold_celsius': 72.0,
            'low_memory_warning_mb': 2000
        }
    }
    print("\nTesting invalid threads (10)...")
    is_valid = ray.get(manager.verify_config_patch_z3.remote(invalid_threads))
    assert is_valid == False, "Invalid threads (10) was incorrectly accepted"

    # Test case 3: Invalid thermal threshold (> 85)
    invalid_thermal = {
        'hardware_limits': {
            'max_threads': 4,
            'thermal_threshold_celsius': 90.0,
            'low_memory_warning_mb': 2000
        }
    }
    print("\nTesting invalid thermal threshold (90.0)...")
    is_valid = ray.get(manager.verify_config_patch_z3.remote(invalid_thermal))
    assert is_valid == False, "Invalid thermal (90.0) was incorrectly accepted"

    # Test case 4: Invalid low memory warning (< 1000)
    invalid_mem = {
        'hardware_limits': {
            'max_threads': 4,
            'thermal_threshold_celsius': 72.0,
            'low_memory_warning_mb': 500
        }
    }
    print("\nTesting invalid memory threshold (500)...")
    is_valid = ray.get(manager.verify_config_patch_z3.remote(invalid_mem))
    assert is_valid == False, "Invalid memory (500) was incorrectly accepted"

    print("\n✅ Z3 Config Patch Solver verification complete.")

if __name__ == "__main__":
    verify_patch_solver()
    ray.shutdown()
