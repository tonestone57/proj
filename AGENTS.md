# AGENTS.md - SGI Operation Manual (2026 Standard)

This document provides instructions for the SGI (Synthetic General Intelligence) agent operating on Intel i5-8265U hardware.

## Core Principle: Minimum Description Length (MDL)
The agent operates under the **MDL principle**: the best understanding of any data is its shortest possible representation. Every cognitive cycle should aim for maximum structural and neural compression.

## 1. Asynchronous Predictive Workspace (APW)

The system operates as a central **Broadcast Center** (Hub) with **Specialized Actors** (Spokes) communicating over an asynchronous **Message Bus**.

### The Actor Pattern
- **Parallel Execution**: Modules operate as autonomous, concurrent units in isolated processes via **Ray**.
- **Hardware Profile**: 15W TDP limit. Max **4 threads**. 2-4 CPU cores allocated per mission-critical actor.
- **Thermal Guard**: Monitor `monitoring/thermal_guard.py`. If temperature > 78°C, the Hub must delay non-essential tasks.

### The Cognitive Heartbeat
- **Drive Engine**: Evaluates state entropy.
- **High Entropy (>2.0)**: Trigger Re-planning or Research Missions.
- **Low Entropy (<0.5)**: Trigger Sleep Cycle (Consolidation).

## 2. Multi-Stage Agentic RAG Pipeline

### Automated Search & Ingestion
- **Tavily/SearXNG**: Primary tools for web data.
- **License Guardian**: Filter out GPL/LGPL/AGPL content via `SearchActor.license_actor`.
- **JIT Context Compilation**: Distill results into a 400-token **Actionable Spec** (API Cheat Sheet).
- **GraphRAG**: Use **tree-sitter** for AST-based indexing into the **Neural Map**.

### 2026 Compression Standards
- **Reasoning Engine**: BF16 (Q16).
- **Base Model Weights**: NF4.
- **Vector Index (RAG)**: Q8 + Binary Quantization.
- **KV Cache**: FP8 (E4M3).
- **Deep Archive**: LLM-Arithmetic Coding (LLM-Zip) + Zstd-19.

## 3. Self-Improvement & Verification

### Context Integrity Check
- **CodeComp**: Perform Structural Distillation if token entropy is low.
- **LLM-Zip**: Perform Neural Archiving if context exceeds 80% of `MAX_LIMIT`.

### Formal Verification
- **SMT-LIB**: Translate mission-critical logic for **Z3** solver to prove safety/correctness.
- **Digital Twin**: Use **Firecracker** for speculative execution. Rewind state on failure.

## 4. Compliance & Ethics
- **Strict Prohibition**: No GPL, LGPL, or AGPL code.
- **Intel Optimization**: Prioritize `intel/neural-chat-14b-v3-3` in low-bit precision.
- **Code Style**: Prioritize Class Hierarchy Preservation for BeOS/Haiku OS development.
