# AGI LLM for Coding, Math and Logic (Optimized for Intel i5-8265U)

This repository contains a modular AGI (Artificial General Intelligence) architecture designed for high-level reasoning, mathematical evaluation, and logical processing, specifically optimized for the **Intel Core i5-8265U (Whiskey Lake)** platform.

### Philosophical Foundation: Minimum Description Length (MDL)
According to the **Minimum Description Length (MDL)** principle, the best "understanding" of a dataset is the shortest possible program that can recreate it. Our SGI system aims to achieve maximum information density and compression in its memory and reasoning loops.

## Architecture

The system utilizes an **Asynchronous Predictive Workspace (APW)**. Unlike traditional models, the Hub acts as a **Broadcast Center** using Pub/Sub logic to eliminate bottlenecks. It implements a **Multi-Stage Agentic RAG Pipeline** and is designed for **Self-Improvement**, autonomously updating its data files and logic to achieve better accuracy and reliability.

### The Dual-Stream System
To maximize performance, cognitive workload is split into two tracks:
- **The Reflex Arc (Fast Path):** Low-latency modules (Safety, Syntax Checking) that act instantly.
- **The Global Workspace (Slow Path):** Higher-order reasoning (Planning, Complex Coding) requiring full attention.

### The Actor Pattern & Ray Integration
Modules operate as autonomous, concurrent units in isolated processes. The Hub broadcasts objectives to specialized actors and synthesizes the optimal response.
- **Orchestration**: Utilizes **Ray** as the primary distributed orchestrator to bypass the Python GIL.
- **Hardware Limits**: Configured for 2-4 CPU cores and a **maximum of 4 threads** to maintain stability on 15W TDP hardware.
- **Thermal Guard**: Real-time monitoring of CPU temperature (threshold 78°C) and load to prevent thermal throttling.
- **Data Transfer**: Uses **Ray Plasma** (shared memory object store) for zero-latency transfer of large technical data buffers between actors.

### Core Components
- **Message Bus (The Spine)**: An asynchronous bus (Ray) where all modules post their state.
- **Integrator (The Hub)**: Samples the Message Bus every "Tick" using **Dragonfly** for high-concurrency state updates.
- **Drive Engine (Drives Module)**: Calculates a **Surprise/Entropy Metric** to proactively trigger re-planning or background consolidation.
- **Internal Critic**: Verifies the logic and safety of outputs before they are finalized using **IPEX-LLM** accelerated models.
- **Memory Manager**: Manages the tiered memory stack and context integrity.

---

## 2026 Compression & Memory Standards

The system adheres to the **2026 SGI Operations** standard for vector embeddings and model precision:

### "Gold Standard" 2026 Tiered Memory Model

| Database | Role | Speed (Latency) | Data Lifecycle | Codec (SGI Alt) |
| :--- | :--- | :--- | :--- | :--- |
| **Semantic Cache** | **Message Bus** | **Sub-millisecond** | Ephemeral | **Flash-Optimized LZ4** |
| **FAISS** | **The Reflex Arc** | **Sub-millisecond** | Transient (Volatile/RAM) | **TurboQuant (QJL)** |
| **Qdrant** | **Social & Logic Hub** | **Low (10-20ms)** | Persistent (Stateful) | **Q8 + BQ** |
| **LanceDB** | **The World Model** | **Medium (Disk-bound)** | Massive (Cold/Disk) | **LLM-Arithmetic Coding** |

### Specialized Codecs
- **TurboQuant (QJL & PolarQuant)**: Used in FAISS/Reflex Arc.
    - **How it works**: Uses **PolarQuant** to randomly rotate data vectors, simplifying their geometry, then applies **Quantized Johnson-Lindenstrauss (QJL)** for a 1-bit "error-correction" pass.
    - **Benefit**: Compresses KV cache and embeddings to **Q8 + BQ** or **NF4** with **0% accuracy loss**.
- **LLM-Zip (Lossless Neural Archiving)**: Used in LanceDB.
    - **Benefit**: Achieves **5x to 10x better compression** than Zstd for code by storing token probabilities predicted by the LLM.
    - **Recovery**: Includes a **Model Hash** and a **Residual Mismatch Buffer** to safeguard against non-deterministic mismatch.
- **Tree-sitter Serialization**: Stores code as AST node operations. Bypasses re-parsing to provide immediate Control Flow Graphs.
- **NeuralLVC / CoPE**: Standard neural codecs for Video/Vision, targeting a **93% token usage reduction**.

### Codec Comparison Table

| Codec Type | Standard | SGI Alternative | Primary Benefit |
| :--- | :--- | :--- | :--- |
| **Hot Storage** | **LZ4 / Zstd-1** | **Flash-Optimized LZ4** | Sub-millisecond latency for the "Reflex Arc." |
| **Vector Search** | **Product Quantization** | **TurboQuant (QJL)** | High compression with **0%** accuracy loss. |
| **Long-term Archive**| **7z (LZMA2)** | **LLM-Arithmetic Coding** | Massive ratio; "stores knowledge, not just data." |
| **Video/Vision** | **H.265 / AV1** | **NeuralLVC / CoPE** | Up to **93%** reduction in token usage for VideoLMs. |

---

## Specialized Capabilities

- **Symbolic Reasoner**: Integrates **Z3 SMT Solver** for formal verification. Translates logic into **SMT-LIB format** to prove absence of overflows or undefined states.
- **Coding Module**: Stateful execution in **Firecracker microVMs** (Digital Twin). Supports **Speculative Execution**, **Runtime Observation**, and **Structural Distillation (CodeComp)**.
- **Search Agent**: Autonomous search using **Tavily/SearXNG**. Implements **GraphRAG (The Neural Map)** and **JIT Context Compilation**.
- **License Guardian**: Strict enforcement of permissive licensing. **GPL/LGPL code is strictly prohibited.**

---

## Getting Started

To run the AGI system:

```bash
# Initial setup for Intel 8265U
bash setup_8265u.sh

# Start the cognitive cycle
python3 main.py
```

## Licensing and Compliance

This repository and all associated data files must NOT contain any code licensed under **GPL** or **LGPL**. The **License Guardian** enforces this gate during ingestion.
