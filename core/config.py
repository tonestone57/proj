import yaml
import os
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Optional, Any

# Pydantic Models for Schema Validation
class SystemIdentity(BaseModel):
    name: str = "SGI-Alpha"
    mode: str = "Autonomous-Predictive-Workspace"

class HardwareLimits(BaseModel):
    total_cpu_threads: int = 8
    ray_reserved_threads: int = 4
    max_threads: int = Field(4, le=8)
    thermal_threshold_celsius: float = 78.0
    low_memory_warning_mb: int = 2000
    shared_gpu_memory: bool = True

class ActorConfig(BaseModel):
    precision: str
    cpu_cores: int
    priority: int
    load_mode: Optional[str] = None

class CompressionConfig(BaseModel):
    vector_index: str
    kv_cache: str
    reasoning_engine: str
    deep_archive: str
    logs: str

class VectorStoreConfig(BaseModel):
    engine: str
    path: str
    embedding_model: str
    reranker_model: str
    matryoshka_tiers: List[int]

class MemoryManagementConfig(BaseModel):
    active_context_limit: int = 4096
    pruning_threshold_pct: float = 0.80
    summarization_depth: str = "recursive"
    compression: CompressionConfig
    vector_store: VectorStoreConfig

class ComplianceConfig(BaseModel):
    prohibited_licenses: List[str]
    verify_on_ingest: bool = True

class DriveEngineConfig(BaseModel):
    heartbeat_interval_seconds: float = 5.0
    entropy_threshold: float = 0.7
    threshold_replan: float = 2.0
    threshold_consolidate: float = 0.5
    active_inference_cycle_ticks: int = 5

class InferenceConfig(BaseModel):
    primary_model: str
    draft_model: str
    speculative_decoding: bool = True
    wisdom_cache: bool = True

class SGIConfig(BaseModel):
    system_identity: SystemIdentity
    hardware_limits: HardwareLimits
    actors: Dict[str, ActorConfig]
    memory_management: MemoryManagementConfig
    compliance: ComplianceConfig
    drive_engine: DriveEngineConfig
    inference: InferenceConfig

    @classmethod
    def load(cls, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        if data is None:
            raise ValueError("Config file is empty.")
        return cls(**data)

# Load configuration from manifest
CONFIG_PATH = "config.yaml"

try:
    SGI_SETTINGS = SGIConfig.load(CONFIG_PATH)
except (FileNotFoundError, ValidationError, ValueError) as e:
    print(f"[Config] Error loading config: {e}")
    # Fallback or exit? For autonomous system, we might want to exit or use defaults if possible.
    # For now, let's assume config.yaml must exist and be valid.
    raise

# Export global variables for backward compatibility
SYSTEM_NAME = SGI_SETTINGS.system_identity.name
CPU_CORES_MAX = SGI_SETTINGS.hardware_limits.ray_reserved_threads
MAX_THREADS = SGI_SETTINGS.hardware_limits.max_threads
THERMAL_THRESHOLD_C = SGI_SETTINGS.hardware_limits.thermal_threshold_celsius
LOW_MEMORY_THRESHOLD_MB = SGI_SETTINGS.hardware_limits.low_memory_warning_mb

# Entropy/Drive thresholds
THRESHOLD_REPLAN = SGI_SETTINGS.drive_engine.threshold_replan
THRESHOLD_CONSOLIDATE = SGI_SETTINGS.drive_engine.threshold_consolidate

# Heartbeat settings
TICK_INTERVAL = SGI_SETTINGS.drive_engine.heartbeat_interval_seconds

# Context management
CONTEXT_SALIENCY_FLOOR = 0.5
MAX_LIMIT = SGI_SETTINGS.memory_management.active_context_limit

# Workspace settings
WORKSPACE_HISTORY_LIMIT = 100

# Actor specific configs
CORES_CODING = SGI_SETTINGS.actors.get("coding_actor", ActorConfig(precision="Q4_K_M", cpu_cores=2, priority=1)).cpu_cores
CORES_REASONER = SGI_SETTINGS.actors.get("symbolic_reasoner", ActorConfig(precision="sym_int8", cpu_cores=2, priority=1)).cpu_cores
CORES_SEARCH = SGI_SETTINGS.actors.get("search_actor", ActorConfig(precision="Q5_K_M", cpu_cores=1, priority=3)).cpu_cores
