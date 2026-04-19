import yaml
import os

# Load configuration from manifest
CONFIG_PATH = "config.yaml"

if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as f:
        manifest = yaml.safe_load(f)
else:
    manifest = {}

# Hardware & System
SYSTEM_NAME = manifest.get("system_identity", {}).get("name", "SGI-Alpha")
CPU_CORES_MAX = manifest.get("hardware_limits", {}).get("ray_reserved_threads", 3)
MAX_THREADS = manifest.get("hardware_limits", {}).get("max_threads", 3)
THERMAL_THRESHOLD_C = manifest.get("hardware_limits", {}).get("thermal_threshold_celsius", 78.0)
LOW_MEMORY_THRESHOLD_MB = manifest.get("hardware_limits", {}).get("low_memory_warning_mb", 2000)

# Entropy/Drive thresholds
THRESHOLD_REPLAN = manifest.get("drive_engine", {}).get("threshold_replan", 2.0)
THRESHOLD_CONSOLIDATE = manifest.get("drive_engine", {}).get("threshold_consolidate", 0.5)

# Heartbeat settings
TICK_INTERVAL = manifest.get("drive_engine", {}).get("heartbeat_interval_seconds", 5.0)

# Context management
CONTEXT_SALIENCY_FLOOR = 0.5
MAX_LIMIT = manifest.get("memory_management", {}).get("active_context_limit", 4096)

# Workspace settings
WORKSPACE_HISTORY_LIMIT = 100

# Actor specific configs
CORES_CODING = manifest.get("actors", {}).get("coding_actor", {}).get("cpu_cores", 2)
CORES_REASONER = manifest.get("actors", {}).get("symbolic_reasoner", {}).get("cpu_cores", 2)
CORES_SEARCH = manifest.get("actors", {}).get("search_actor", {}).get("cpu_cores", 1)
