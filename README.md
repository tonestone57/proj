# AGI LLM for Coding, Math and Logic

This repository contains a modular AGI (Artificial General Intelligence) architecture designed for high-level reasoning, mathematical evaluation, and logical processing.

## Architecture

The system utilizes an **Asynchronous Predictive Workspace (APW)**. Unlike traditional models, the Hub acts as a **Broadcast Center** using Pub/Sub logic to eliminate bottlenecks. It implements a **Multi-Stage Agentic RAG Pipeline** and is designed for **Self-Improvement**, autonomously updating its data files and logic to achieve better accuracy and reliability.

### The Dual-Stream System
To maximize performance, cognitive workload is split into two tracks:
- **The Reflex Arc (Fast Path):** Low-latency modules (Safety, Syntax Checking) that act instantly.
- **The Global Workspace (Slow Path):** Higher-order reasoning (Planning, Complex Coding) requiring full attention.

### Core Components
- **Message Bus (The Spine)**: An asynchronous bus (Ray or NATS) where all modules post their state.
- **Integrator (The Hub)**: Samples the Message Bus every "Tick" using **Dragonfly** for high-concurrency state updates.
- **Drive Engine (Drives Module)**: Calculates a **Surprise/Entropy Metric** to proactively trigger re-planning or background consolidation.
- **Internal Critic**: Verifies the logic and safety of outputs before they are finalized.
- **Scratchpad Memory**: A dedicated working memory area for intermediate reasoning steps.

### Dynamic Processing System (DPS)
- **Task Router**: Directs messages to the appropriate modules.
- **Priority Engine**: Computes dynamic priorities based on context and urgency.
- **Attention Gate**: Filters and amplifies signals to manage cognitive load. Integrates with the **Ethics** module for proactive vetting.

### Specialized Modules
- **Symbolic Reasoner**: Handles mathematical and logical queries. Integrates **SMT Solvers (Z3)** for formal verification by translating logic into **SMT-LIB format** to prove the absence of undefined states or overflows. Supports **LLM-Zip** (Lossless Neural Archiving) for deep session decompression.
- **Coding Module**: Executes and verifies code in a **Stateful Digital Twin** (Firecracker microVMs). It calculates a **Confidence Score** and triggers **Research Missions** (Active Learning) when entropy is high. Implements **CodeComp** (AST-Aware KV Cache Compression).
- **Search Agent**: Performs autonomous online searches using **Tavily** and **SearXNG**. Implements **GraphRAG** (The "Neural Map") and **JIT Context Compilation** (Synthesized Micro-Contexts). Includes a **License Guardian Classifier Gate** (No GPL).
- **Critic**: Evaluates the reasoning of other modules to ensure accuracy and safety.
- **Vision Module**: Processes visual inputs.
- **Planner**: Generates step-by-step plans to achieve goals.
- **Self Model**: Tracks the AGI's internal state and identity.
- **World Model**: Maintains a persistent representation of reality.
- **Social Module**: Inferred beliefs, intentions, and social interactions.

---

## RAG & Knowledge Extraction (GGUF)

To expand the AGI's knowledge base beyond its core modules, the system supports **Retrieval-Augmented Generation (RAG)** by extracting data from **GGUF** models.

### Extraction Process
1. **Probe**: The GGUF model is prompted to generate exhaustive information on target topics.
2. **Embed**: Generated text is converted into mathematical vectors (embeddings).
3. **Compress**: Vectors are stored in optimized formats for high-speed retrieval.

### Storage Options
The AGI utilizes the **"Gold Standard" 2026 Tiered Memory Model**:

| Database | Role | Speed (Latency) | Data Lifecycle |
| :--- | :--- | :--- | :--- |
| **FAISS** | **The Reflex Arc** | **Sub-millisecond** | Transient (Volatile/RAM) |
| **Qdrant** | **The Social & Logic Hub** | **Low (10-20ms)** | Persistent (Stateful/Index) |
| **LanceDB** | **The World Model** | **Medium (Disk-bound)** | Massive (Cold/Disk) |

- **FAISS**: Embedded in the Hub for instant thought-deduplication. Uses **TurboQuant** (Entropy-Targeted Quantization) for efficient storage (2-bit to FP16 tiering).
- **Qdrant**: Primary store for active reasoning and payload filtering.
- **LanceDB**: The "Cortical Archive" for storing terabytes of technical documentation. Supports **LLM-Arithmetic Coding** (Lossless Neural Archiving) for neural archiving.
- **NebulaGraph/TuGraph**: Stores the **Neural Map** (AST-based relationships) for GraphRAG.

---

## Getting Started

To run the AGI system:

```bash
python3 main.py
```

## Capabilities

The AGI system focuses primarily on high-stakes intellectual domains: **C, C++, Python, Rust, Javascript, Typescript, SQL, PHP, C#, Mathematics, and Logic**.

### Mathematics and Logic
The `SymbolicReasoner` module evaluates complex expressions and performs formal reasoning:
- **Arithmetic**: `math.factorial(5)`, `math.sqrt(16)`
- **Logic**: `True and (False or True)`
- **Formal Verification**: Integration with **Z3 SMT Solver** to prove code correctness and safety at a mathematical level.

### Coding & Self-Improvement
The `CodingModule` executes code across supported languages and specialized APIs.
- **Polyglot Execution**: Sandboxed execution and testing.
- **Stateful Sandbox Persistence**: Uses **AWS Firecracker** microVMs as a **Persistent Digital Twin**.
- **Specialized APIs**: Deep integration with **BeOS** and **Haiku OS** APIs. Prioritizes **Class Hierarchy Preservation** (virtual functions) during distillation.
- **Cognitive Heartbeat**: Runs a proactive loop based on **System Entropy**.
- **Context Integrity**: Triggers **Structural Distillation** (CodeComp) if token entropy is low, or **Neural Offloading** (LLM-Zip) if context is full.

## Directory Structure

```text
├── core/
│   ├── message_bus/       # Pub/Sub event router (Redis/ZeroMQ)
│   ├── heartbeat.py       # The autonomous cognitive loop
│   └── drives.py          # Entropy/Surprise calculator (Curiosity Drive)
├── actors/                # Formerly 'modules' - Independent processes
│   ├── coding_actor.py    # Polyglot sandbox & Stateful Digital Twin (CodeComp)
│   ├── reasoner_actor.py  # Z3/Lean/SMT-LIB integration (LLM-Zip)
│   ├── search_actor.py    # Tavily/GraphRAG & JIT Context Compilation
│   └── critic_actor.py    # Output verification
├── memory/
│   ├── cache/             # Sub-millisecond Semantic Cache (TurboQuant)
│   ├── short_term/        # FAISS (Active Context)
│   ├── long_term/         # LanceDB (Archived Context)
│   ├── memory_manager.py  # Sleep Cycles & Context Integrity Check
│   └── scratchpad.py      # Transient reasoning steps
├── world_model/           # External reality & Runtime Digital Twin
└── safety_ethics/         # License compliance (License Guardian) and alignment
```

---

## Licensing and Compliance

**Strict Requirement**: This repository and all associated data files must NOT contain any code licensed under **GPL** or **LGPL**. All contributions and indexed data must adhere to permissive licenses (e.g., MIT, Apache 2.0, BSD) or be original works. The **License Guardian** enforces this gate during ingestion.
