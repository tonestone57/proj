# AGI LLM for Coding, Math and Logic (Optimized for Intel i5-8265U)

This repository contains a modular AGI (Artificial General Intelligence) architecture designed for high-level reasoning, mathematical evaluation, and logical processing, specifically optimized for the **Intel Core i5-8265U (Whiskey Lake)** platform.

### Philosophical Foundation: Minimum Description Length (MDL)
According to the **Minimum Description Length (MDL)** principle, the best "understanding" of a dataset is the shortest possible program that can recreate it. Our SGI system aims to achieve maximum information density and compression in its memory and reasoning loops.

## Architecture

The system utilizes an **Asynchronous Predictive Workspace (APW)**. Unlike traditional models, the Hub acts as a **Broadcast Center** using Pub/Sub logic to eliminate bottlenecks. It implements a **Multi-Stage Agentic RAG Pipeline** and is designed for **Self-Improvement**, autonomously updating its data files and logic to achieve better accuracy and reliability.

### The Actor Pattern & Ray Integration
Modules operate as autonomous, concurrent units in isolated processes. The Hub broadcasts objectives to specialized actors and synthesizes the optimal response.
- **Orchestration**: Utilizes **Ray** as the primary distributed orchestrator.
- **Hardware Limits**: Configured for 2-4 CPU cores and a **maximum of 4 threads** to maintain stability on 15W TDP hardware.
- **Thermal Guard**: Real-time monitoring of CPU temperature (threshold 78°C) and load to prevent thermal throttling.

### Core Components
- **Message Bus (The Spine)**: An asynchronous bus (Ray) where all modules post their state.
- **Integrator (The Hub)**: Samples the Message Bus every "Tick" using **Dragonfly** for high-concurrency state updates.
- **Drive Engine (Drives Module)**: Calculates a **Surprise/Entropy Metric** to proactively trigger re-planning or background consolidation.
- **Internal Critic**: Verifies the logic and safety of outputs before they are finalized using **IPEX-LLM** accelerated models.
- **Memory Manager**: Manages the tiered memory stack and context integrity.

---

## 2026 Compression & Memory Standards

The system adheres to the **2026 SGI Operations** standard for vector embeddings and model precision:

| Component | Standard | Reasoning |
| :--- | :--- | :--- |
| **Reasoning Engine** | **BF16 (Q16)** | Zero-compromise logic & proof-chaining. |
| **Base Model Weights** | **NF4** | Information-theoretically optimal for Gaussian weights. |
| **Vector Index (RAG)** | **Q8 + Binary Quantization** | INT8 for accuracy, Binary for massive scale. |
| **KV Cache (Memory)** | **FP8 (E4M3)** | High dynamic range for "spiky" activations. |
| **Search/Text Logs** | **Zstd-19** | Standard high-ratio compression for raw logs. |

### Tiered Memory Model
1. **Tier 1 (Ephemeral)**: **Flash-Optimized LZ4** for the Message Bus.
2. **Tier 2 (Active Context)**: **TurboQuant (QJL)** for the KV cache/FAISS.
3. **Tier 3 (Deep Archive)**: **LLM-Arithmetic Coding** (LLM-Zip) in **LanceDB**.

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
