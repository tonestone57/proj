import sys
import os
from pydantic import ValidationError
import yaml

# Ensure we can import from core
sys.path.append(os.getcwd())

def verify_config():
    print("--- Verifying Config Loading ---")
    try:
        from core.config import SGI_SETTINGS, SYSTEM_NAME, MAX_THREADS
        print(f"Successfully loaded SGI_SETTINGS: {SGI_SETTINGS.system_identity.name}")
        print(f"SYSTEM_NAME: {SYSTEM_NAME}")
        print(f"MAX_THREADS: {MAX_THREADS}")

        assert SYSTEM_NAME == SGI_SETTINGS.system_identity.name
        assert MAX_THREADS == SGI_SETTINGS.hardware_limits.max_threads
        print("✅ Config globals match SGI_SETTINGS.")
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        sys.exit(1)

def verify_invalid_config():
    print("\n--- Verifying Invalid Config Handling ---")
    invalid_config = {
        "system_identity": {"name": "SGI-Fail"},
        "hardware_limits": {"max_threads": 10},  # Fails le=8 constraint
        "actors": {},
        "memory_management": {},
        "compliance": {},
        "drive_engine": {},
        "inference": {}
    }

    with open("config_invalid.yaml", "w") as f:
        yaml.dump(invalid_config, f)

    try:
        from core.config import SGIConfig
        SGIConfig.load("config_invalid.yaml")
        print("❌ Error: Invalid config did not trigger validation error.")
        sys.exit(1)
    except ValidationError as e:
        print(f"✅ Successfully caught validation error as expected: {e.errors()[0]['msg']}")
    except Exception as e:
        print(f"❌ Unexpected error type: {type(e).__name__}: {e}")
        sys.exit(1)
    finally:
        if os.path.exists("config_invalid.yaml"):
            os.remove("config_invalid.yaml")

if __name__ == "__main__":
    verify_config()
    verify_invalid_config()
    print("\nConfig verification complete.")
