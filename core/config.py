# SGI System Configuration Constants

# Entropy/Drive thresholds
THRESHOLD_REPLAN = 2.0
THRESHOLD_CONSOLIDATE = 0.5

# Heartbeat settings
TICK_INTERVAL = 5.0 # Seconds

# Context management
CONTEXT_SALIENCY_FLOOR = 0.5
MAX_LIMIT = 8192 # Token limit

# Workspace settings
WORKSPACE_HISTORY_LIMIT = 100

# Compression & Data Integrity
MODEL_HASH = "8a2b3c4d5e6f7g8h" # Current LLM weight hash for neural codecs
COMPRESSION_TIERING_ENABLED = True
