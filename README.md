# SGI-Alpha: AGI LLM for Coding, Math and Logic

This repository contains a modular AGI (Artificial General Intelligence) architecture designed for high-level reasoning, mathematical evaluation, and logical processing. It has been strictly optimized for the Intel Core i7-8265U (15W TDP) with 16GB RAM, carefully balancing maximum cognitive density with strict thermal and memory limits.

## Philosophical Foundation: Minimum Description Length (MDL)

According to the Minimum Description Length (MDL) principle, the best "understanding" of a dataset is the shortest possible program that can recreate it. Our SGI system aims to achieve maximum information density and compression in its memory and reasoning loops.

## Architecture

The system utilizes an Asynchronous Predictive Workspace (APW). Unlike traditional models, the Hub acts as a Broadcast Center using Pub/Sub logic to eliminate bottlenecks. It implements a Multi-Stage Agentic RAG Pipeline and is designed for Self-Improvement, autonomously updating its data files and logic. The engine is hard-capped to utilize a maximum of 3 threads to maintain system stability and thermal headroom.

### The Dual-Stream System

To maximize performance and prevent thermal throttling on the 15W i7-8265U, cognitive workload is split into two tracks:

- **The Reflex Arc (Fast Path)**: Low-latency modules (Safety, Syntax Checking, Thermal Guard) that act instantly.
- **The Global Workspace (Slow Path)**: Higher-order reasoning (Planning, Complex Coding) requiring full attention, actively managed by a Thermal Circuit Breaker.

### Core Components

- **Message Bus (The Spine)**: An asynchronous bus (Ray or NATS) where all modules post their state.
- **Integrator (The Hub)**: Samples the Message Bus every "Tick" using Dragonfly for high-concurrency state updates.
- **Drive Engine (Drives Module)**: Calculates a Surprise/Entropy Metric to proactively trigger re-planning or background consolidation.
- **Internal Critic**: Verifies the logic and safety of outputs before they are finalized.
- **Scratchpad Memory**: A dedicated working memory area for intermediate reasoning steps.

### Dynamic Processing System (DPS)

- **Task Router**: Directs messages to the appropriate modules.
- **Priority Engine**: Computes dynamic priorities based on context and urgency.
- **Attention Gate**: Filters and amplifies signals to manage cognitive load. Integrates with the Ethics module for proactive vetting.
- **Thermal Guard**: Monitors CPU temperature and load, pausing complex tasks if thresholds are exceeded to prevent thermal throttling.

### Specialized Modules

- **Symbolic Reasoner**: Handles mathematical and logical queries. Integrates SMT Solvers (Z3) for formal verification. Operates natively in sym_int8 precision for AVX2 efficiency.
- **Coding Module**: Executes and verifies code in a Stateful Digital Twin (Firecracker microVMs). Uses Q4_K_M precision for weights and sym_int8 for reasoning to maintain a consistent "Cognitive Heartbeat." Implements CodeComp (AST-Aware KV Cache Compression).
- **Search Agent**: Performs autonomous online searches using Tavily and SearXNG at Q5_K_M precision. Implements GraphRAG and JIT Context Compilation. Includes a License Guardian Classifier Gate (No GPL).
- **Critic & Planner**: Evaluates reasoning for accuracy and generates step-by-step plans.
- **Self, World, & Social Models**: Tracks internal state, external reality, and infers social/user intentions.

## RAG & Knowledge Extraction (GGUF)

To expand the AGI's knowledge base beyond its core modules, the system supports RAG by extracting data from GGUF models, utilizing a robust compression pipeline tailored to mobile CPUs.

## Technical Specifications
- **CPU**: Intel Core i7-8265U (Whiskey Lake)
- **Memory**: 16GB DDR4
- **Precision Tiers**:
    - **Weight Storage**: Q4_K_M (Balanced 4-bit GGUF/IPEX)
    - **Search Index**: Q5_K_M (Optimized for Retrieval, 5-bit)
    - **Reasoning/Math**: sym_int8 (Symmetric 8-bit)
    - **KV Cache**: sym_int8 (Per-Channel Scaling)
- **RAG Engine**: LanceDB (Archive) + FAISS (Reflex)

### Hardware-Aware Precision Standard (i7-8265U Optimized)

To fit within the memory bandwidth and thermal envelope of the 8265U, the model forces specific quantization formats:

| Component | Format | Reasoning |
| :--- | :--- | :--- |
| Reasoning (Brain) | sym_int8 | Maximizes AVX2 throughput by removing zero-point offsets. |
| Weights (Storage) | Q4_K_M | Optimized for Intel AVX2 instructions (4-bit); ensures zero-lag activation. |
| Search Results | Q5_K_M | Optimized for online data indexing (5-bit). |
| KV Cache (Memory) | sym_int8 | Handles "spiky" data with Per-Channel Scaling ($S_i = \frac{\max(|x_i|)}{127}$). |
| Index (RAG) | sym_int8 + BQ | sym_int8 for distance calculations (Dot Product), Binary for scale. |
| Search/Text Logs | Zstd-19 | Standard high-ratio compression for raw text/logs. |

### The Tiered Memory Model & Codecs

| Database | Role | Speed (Latency) | Data Lifecycle | Codec (SGI Alt) |
| :--- | :--- | :--- | :--- | :--- |
| Semantic Cache | Message Bus | Sub-millisecond | Ephemeral | Flash-Optimized LZ4 |
| FAISS | The Reflex Arc | Sub-millisecond | Transient (RAM) | TurboQuant (QJL) |
| Qdrant | The Logic Hub | Low (10-20ms) | Persistent (Index) | sym_int8 + BQ |
| LanceDB | The World Model | Medium (Disk) | Massive (Cold) | LLM-Arithmetic Coding |

- **FAISS**: Embedded in the Hub for instant thought-deduplication. Uses TurboQuant (with QJL & PolarQuant) to rotate data vectors and apply error-correction, compressing vectors to 3-bit/4-bit with 0% accuracy loss.
- **LanceDB**: The "Cortical Archive." Supports LLM-Arithmetic Coding (Lossless Neural Archiving/LLM-Zip), achieving 5x to 10x better compression than Zstd/7z by storing token probabilities predicted by the LLM.
- **NebulaGraph/TuGraph**: Stores the Neural Map for GraphRAG. Uses Tree-sitter Serialization to compactly store code as Abstract Syntax Tree (AST) node operations, bypassing re-parsing for immediate Control Flow Graphs.

## Model: Apriel-1.6-15B-Thinker
Apriel-1.6-15B-Thinker is required for its high reasoning density and optimized parameter footprint, ideal for the i7-8265U's 15W TDP. It is utilized across all cognitive actors as a shared "Singleton Model" via the ModelRegistry to minimize RAM usage and prevent system crashes on 16GB hardware.

## Getting Started

To run the SGI-Alpha system on Intel i7-8265U:

1. **Setup Environment**:
   ```bash
   bash setup_8265u.sh
   ```
2. **Launch System**:
   ```bash
   python3 main.py
   ```

## Capabilities

The AGI system focuses primarily on high-stakes intellectual domains: C, C++, Python, Rust, Javascript, Typescript, SQL, PHP, C#, Mathematics, and Logic.

### Mathematics and Logic

The SymbolicReasoner evaluates complex expressions and performs formal reasoning:

- **Arithmetic**: `math.factorial(5)`, `math.sqrt(16)`
- **Logic**: `True and (False or True)`
- **Formal Verification**: Integration with Z3 SMT Solver to prove code correctness mathematically, ensuring no undefined states or overflows.

### Coding & Self-Improvement

- **Polyglot Execution**: Sandboxed execution and testing.
- **Stateful Sandbox Persistence**: Uses AWS Firecracker microVMs as a Persistent Digital Twin.
- **Specialized APIs**: Deep integration with BeOS and Haiku OS APIs. Prioritizes Class Hierarchy Preservation (virtual functions) during distillation.
- **Context Integrity**: Triggers Structural Distillation (CodeComp) if token entropy is low, or Neural Offloading (LLM-Zip) if context is full.

## Directory Structure

```
├── core/
│   ├── message_bus/       # Pub/Sub event router (Redis/ZeroMQ)
│   ├── heartbeat.py       # The autonomous cognitive loop (Thermal aware)
│   ├── drives.py          # Entropy/Surprise calculator (Curiosity Drive)
│   ├── model_registry.py  # Shared Singleton Model Provider
│   └── workspace.py       # Global state management
├── actors/                # Independent processes (capped at 3 threads)
│   ├── coding_actor.py    # Polyglot sandbox & Stateful Digital Twin
│   ├── reasoner_actor.py  # Z3/Lean/SMT-LIB integration (sym_int8)
│   ├── search_actor.py    # Tavily/GraphRAG & JIT Context Compilation
│   └── critic_actor.py    # Output verification
├── memory/
│   ├── cache/             # Sub-millisecond Semantic Cache (Flash LZ4)
│   ├── short_term/        # FAISS (Active Context - TurboQuant)
│   ├── long_term/         # LanceDB (Archived Context - LLM-Zip)
│   ├── memory_manager.py  # Sleep Cycles & RAM Guard (2000MB)
│   └── scratchpad.py      # Transient reasoning steps
├── world_model/           # External reality & Runtime Digital Twin
└── safety_ethics/         # Thermal Guard, License Guardian, and alignment
```

## Licensing and Compliance

**Strict Requirement**: This repository and all associated data files must NOT contain any code licensed under GPL or LGPL. All contributions and indexed data must adhere to permissive licenses (e.g., MIT, Apache 2.0, BSD) or be original works. The License Guardian enforces this gate during ingestion.
