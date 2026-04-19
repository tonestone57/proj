import yaml
import os

# Path to the central manifest
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    return {}

_config = load_config()

# Entropy/Drive thresholds
THRESHOLD_REPLAN = _config.get('drive_engine', {}).get('entropy_threshold', 2.0)
THRESHOLD_CONSOLIDATE = 0.5

# Heartbeat settings
TICK_INTERVAL = _config.get('drive_engine', {}).get('heartbeat_interval_seconds', 5.0)

# Context management
CONTEXT_SALIENCY_FLOOR = 0.5
MAX_LIMIT = 8192 # Token limit
ACTIVE_CONTEXT_LIMIT = _config.get('memory_management', {}).get('active_context_limit', 2048)
PRUNING_THRESHOLD_PCT = _config.get('memory_management', {}).get('pruning_threshold_pct', 0.80)

# Workspace settings
WORKSPACE_HISTORY_LIMIT = 100

# Hardware Resource Allocation (8265U - 15W TDP)
TOTAL_CPU_THREADS = _config.get('hardware_limits', {}).get('total_cpu_threads', 8)
RAY_RESERVED_THREADS = _config.get('hardware_limits', {}).get('ray_reserved_threads', 6)
THERMAL_THRESHOLD_CELSIUS = _config.get('hardware_limits', {}).get('thermal_threshold_celsius', 78.0)
LOW_MEMORY_WARNING_MB = _config.get('hardware_limits', {}).get('low_memory_warning_mb', 800)

# Hardware limits (2026 Standards)
CPU_CORES_MIN = _config.get('hardware_limits', {}).get('cpu_cores_min', 2)
CPU_CORES_MAX = _config.get('hardware_limits', {}).get('cpu_cores_max', 4)
MAX_THREADS = _config.get('hardware_limits', {}).get('max_threads', 4)

# Actor resource allocation
CORES_SYMBOLIC = _config.get('actors', {}).get('symbolic_reasoner', {}).get('cpu_cores', 2)
CORES_SOCIAL = _config.get('actors', {}).get('social_intent_agent', {}).get('cpu_cores', 1)
CORES_SEARCH = _config.get('actors', {}).get('search_ingestion_spoke', {}).get('cpu_cores', 1)
CORES_CODING = _config.get('actors', {}).get('coding_actor', {}).get('cpu_cores', 2)
CORES_CRITIC = 2
