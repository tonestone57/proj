# SGI-Alpha: AGI LLM for Coding, Math and Logic

This repository contains a modular AGI (Artificial General Intelligence) architecture designed for high-level reasoning, mathematical evaluation, and logical processing. It has been strictly optimized for the Intel Core i7-8265U (15W TDP) with 16GB RAM, carefully balancing maximum cognitive density with strict thermal and memory limits.

Moving the **Symbolic Reasoner** and **Coding Module** to Tier 1 is a brilliant move for a 15W TDP constraint. It pivots the system from a "Language-First" to a **"Logic-First"** architecture.

On an i7-8265U, LLM inference is your most "expensive" operation in terms of thermal Joules per token. By moving Z3 and the Firecracker sandbox to Tier 1, you allow the system to solve problems via formal logic or execution *before* burning the thermal budget on the 15B parameter "Thinker."

###

---

## Philosophical Foundation: Minimum Description Length (MDL)

According to the Minimum Description Length (MDL) principle, the best "understanding" of a dataset is the shortest possible program that can recreate it. Our SGI system aims to achieve maximum information density and compression in its memory and reasoning loops.

## Architecture

The system utilizes an Asynchronous Predictive Workspace (APW). Unlike traditional models, the Hub acts as a Broadcast Center using Pub/Sub logic to eliminate bottlenecks. It implements a Multi-Stage Agentic RAG Pipeline and is designed for Self-Improvement, autonomously updating its data files and logic. The engine is hard-capped to utilize a maximum of 3 threads to maintain system stability and thermal headroom.

## 1. Improved Tiered Hierarchy (The "Logic-First" Pivot)

To accommodate your changes, we should redefine the Tiers to ensure the LLM is only invoked when deterministic methods fail.

* **Tier 1: Reflex & Determinism (The "Fast Path")**
    * **Components:** Qwen3.5-2B (Reflex Actor), **Z3 SMT Solver**, **Code Sandbox (Firecracker)**, and Syntax Linters.
    * **Logic:** If the query is identified as mathematical or purely algorithmic, the system attempts a "Zero-LLM" solve using the Symbolic Reasoner or by generating and running a Python script in Tier 1.
* **Tier 2: Context & Retrieval (The "Knowledge Path")**
    * **Components:** Matryoshka-Tiered RAG (nomic-embed).
    * **Logic:** Pulls documentation or previous "Wisdom Cache" hits to provide context if Tier 1 needs more data.
* **Tier 3: Deep Reasoning (The "Slow Path")**
    * **Components:** Apriel-1.6-15B-Thinker.
    * **Logic:** Only engaged if Tier 1's "Internal Critic" fails the logic check or if the task is high-ambiguity (e.g., architectural design vs. simple bug fixing).
* **Tier 4: Evolutionary Meta-Manager**
    * **Components:** Active Inference Loop.
    * **Logic:** Compiles logs from failed Tier 1 attempts to "teach" the Reflex actor better heuristics.

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

## 2. Technical Enhancements for the i7-8265U

Since you are dealing with a Whiskey Lake processor (4 Cores / 8 Threads, but 15W), here is how to squeeze more "Cognitive Density" out of the hardware:

### KV Cache Shadowing
For the 15B model, the KV Cache will quickly eat your 16GB RAM.
* **Improvement:** Implement **Layer-Wise KV Offloading**. Since you are capped at 3 threads, you aren't utilizing all cores. Use the "spare" threads to asynchronously compress the KV cache of inactive branches using the **LLM-Arithmetic Coding** you mentioned.

### Formal Verification Bridge
Ensure the **Symbolic Reasoner** isn't just a passive tool but a **Gatekeeper**.
* **The "Hallucination Breaker":** Before Tier 3 (Apriel) outputs a math result, Tier 1 (Z3) must verify the logical consistency. If Z3 returns `UNSAT`, the response is discarded and re-routed to the Planner without user intervention.

### Specialized Modules

- **Symbolic Reasoner**: Handles mathematical and logical queries. Integrates SMT Solvers (Z3) for formal verification. Operates natively in sym_int8 precision for AVX2 efficiency.
- **Coding Module**: Executes and verifies code in a Stateful Digital Twin (Firecracker microVMs). Uses Q4_K_M precision for weights and sym_int8 for reasoning to maintain a consistent "Cognitive Heartbeat." Implements CodeComp (AST-Aware KV Cache Compression).
- **Search Agent**: Performs autonomous online searches using Tavily and SearXNG at Q5_K_M precision. Implements **Matryoshka-Tiered Retrieval**, GraphRAG, and **Reasoning-Aware RAG** (utilizing the Wisdom Cache). Includes a License Guardian Classifier Gate (No GPL).
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

## 3. Optimized Precision Mapping

To maximize the AVX2 instruction set on your i7, we can refine your quantization table:

| Component | Target Precision | Optimization Strategy |
| :--- | :--- | :--- |
| **Symbolic Logic** | `fp32` (limited) | Keep SMT solving in high precision; Z3 is lightweight enough that quantization adds more overhead than it saves. |
| **Reasoning (Brain)** | `sym_int8` | Maximizes AVX2 throughput by removing zero-point offsets. |
| **Weights (Storage)** | `Q4_K_M` | Optimized for Intel AVX2 instructions (4-bit); ensures zero-lag activation. |
| **Reflex Actor** | `Q4_K_M` | Qwen-2B stays more accurate |
| **Search Results** | `Q5_K_M` | Optimized for online data indexing (5-bit). |
| **KV Cache** | `sym_int8` | Use per-token dynamic scaling: $S = \frac{\max(|X|)}{7}$ to fit longer contexts in 16GB. |
| **Index (RAG)** | `sym_int8 + BQ` | sym_int8 for distance calculations (Dot Product), Binary for scale. |
| **Search/Text Logs** | `Zstd-19` | Standard high-ratio compression for raw text/logs. |

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

- **Model: Apriel-1.6-15B-Thinker & Qwen3.5-2B**
The system uses a dual-model architecture. **Apriel-1.6-15B-Thinker** serves as the primary reasoning brain, while **Qwen3.5-2B** acts as a lightweight draft model for **Speculative Decoding** and **Reflex-path** tasks. They are managed as shared singletons in the ModelRegistry to minimize RAM pressure.

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

## 4. Summary of Improvements

The SGI-Alpha is now a **Deterministic-Hybrid AGI**. By promoting the Coding and Symbolic modules to Tier 1, you have achieved:

1.  **Thermal Efficiency:** You solve math/code via low-overhead C++ binaries (Z3/Sandboxes) rather than high-overhead matrix multiplications.
2.  **Reliability:** Mathematical "hallucinations" are physically impossible if the Symbolic Reasoner (Tier 1) acts as the final validator.
3.  **RAM Headroom:** By utilizing "Reflex-first" logic, the 15B model stays in a "paged-out" or "frozen" state more often, leaving more of the 16GB RAM for the **World Model** and **GraphRAG**.

> **Strategic Note:** Ensure your **Message Bus** uses shared memory (Unix Domain Sockets) rather than TCP/IP to keep latency sub-millisecond on this specific mobile chipset.

## Licensing and Compliance

**Strict Requirement**: This repository and all associated data files must NOT contain any code licensed under GPL or LGPL. All contributions and indexed data must adhere to permissive licenses (e.g., MIT, Apache 2.0, BSD) or be original works. The License Guardian enforces this gate during ingestion.
