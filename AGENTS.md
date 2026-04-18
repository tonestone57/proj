# Agent Development Guidelines (SGI Roadmap)

This file provides instructions for the AGI (or Synthetic General Intelligence - SGI) to follow during its autonomous development and self-improvement cycles.

## 1. Asynchronous Predictive Workspace (APW)

The system operates as a central **Broadcast Center** (Hub) with **Specialized Actors** (Spokes) communicating over an asynchronous **Message Bus**.

### The Actor Pattern
- **Parallel Execution**: Modules operate as autonomous, concurrent units.
- **Implementation**: Utilize **Ray** as the primary distributed orchestrator.

### The Cognitive Heartbeat (Curiosity Drive)
- The system runs a **Heartbeat Loop** to maintain proactivity.
- **Drive Engine**: Evaluates the system's state using a **Surprise/Entropy Metric**.
- **High Entropy**: Trigger re-planning or an **Active Learning Research Mission**.
- **Low Entropy**: Trigger a **Sleep Cycle** for background consolidation.

## 2. Multi-Stage Agentic RAG Pipeline

The system must follow an iterative loop: **Reason → Search → Ingest → Index → Generate**.

### Automated Online Search
- **Primary Tool**: Use **Tavily AI** for 90% of tasks.
- **JIT Context Compilation**: Move from "Retrieved Chunks" to "Synthesized Micro-Contexts." Distill multiple search results into a single, high-density **Actionable Spec** (e.g., a 400-token API Cheat Sheet for Haiku OS).
- **GraphRAG (The Neural Map)**: Use **tree-sitter** for **AST-based Indexing** to parse code into a graph of dependencies. Store relationships in **NebulaGraph** or **TuGraph**.

### Data Ingestion & Indexing
- **Cleaning**: Distill HTML into clean Markdown before indexing.
- **Entropy-Targeted Quantization (TurboQuant)**:
    - **High Entropy Data**: Store at **FP16** or **INT8**.
    - **Low Entropy Data**: Store at **2-bit (Quantized Johnson-Lindenstrauss)**.
- **License Guardian**: Every snippet must pass through a specialized **License Classifier Gate**.

## 3. Self-Improvement & Verification

### Context Pruning & Integrity Check
- **Trigger**: Instead of a simple 80% limit, use a **Context Integrity Check**:
    - If `token_entropy < CONTEXT_SALIENCY_FLOOR`: Trigger **Structural Distillation** (CodeComp).
    - If `len(context) > MAX_LIMIT * 0.8`: Trigger **Neural Offloading** (LLM-Zip).
- **Structural KV Cache Compression (CodeComp)**: Use a **Code Property Graph (CPG)** to identify the "Control Flow Skeleton." Protect function signatures, return types, and control logic (if/while) while evicting boilerplate.
- **Class Hierarchy Preservation**: For object-oriented APIs (like BeOS/Haiku), always retain `virtual` function overrides during distillation to preserve the code schema.

### The "Internal Critic" Loop
- Every output must be verified by a `Critic` agent or the `World Model`.

### Formal Verification
- **SMT Solver (Z3)**: For mission-critical logic, translate code logic into **SMT-LIB format**.

## 4. Memory Management

### Tiered Context System
1. **Reflex (FAISS)**: Sub-millisecond thought-deduplication using **TurboQuant**.
2. **Active (Qdrant)**: High-accuracy structured filtering.
3. **Archive (LanceDB)**: Zero-copy disk storage for massive RAG documentation.
4. **Neural Map (NebulaGraph/TuGraph)**: Stores AST relationships.

### Lossless Neural Archiving (LLM-Zip)
- Use **Neural Compression** for long-term logs. Encode history into dense, non-human-readable representations (arithmetic coding via LLM probabilities).
- **Decompression**: When needed, decompress back into the original token stream with **0% information loss**.

### Sleep Cycles (Consolidation)
- During **Low Entropy** periods:
    1. Review `Scratchpad` and `Active Context` for patterns.
    2. **Synthesize** a new "Knowledge Base Entry."
    3. **Synaptic Pruning**: Archive raw logs and keep only synthesized lessons.

## 5. Digital Twin & Runtime
- **World Model**: Tracks reality and API states.
- **Stateful Sandbox Persistence**: Use **AWS Firecracker** microVMs as a **Persistent Digital Twin**. Perform **Speculative Execution** and rewind if entropy spikes.

## 6. Compliance & Ethics
- **Strictly Prohibited**: Never integrate or generate code licensed under **GPL** or **LGPL**.
- **Domain Focus**: C, C++, Python, Rust, Javascript, Typescript, SQL, PHP, C#, BeOS/Haiku OS APIs, Mathematics, and Logic.
