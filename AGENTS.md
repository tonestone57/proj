# Agent Development Guidelines (SGI Roadmap)

This file provides instructions for the AGI (or Synthetic General Intelligence - SGI) to follow during its autonomous development and self-improvement cycles.

## 1. Asynchronous Predictive Workspace (APW)

The system operates as a central **Broadcast Center** (Hub) with **Specialized Actors** (Spokes) communicating over an asynchronous **Message Bus**.

### The Actor Pattern
- **Parallel Execution**: Modules operate as autonomous, concurrent units. The Hub broadcasts objectives to specialized actors and synthesizes the optimal response.
- **Implementation**: Utilize **Ray** as the primary distributed orchestrator. Actors must run in isolated processes to prevent CPU-heavy workloads from blocking the central Message Bus.

### The Cognitive Heartbeat (Curiosity Drive)
- The system runs a **Heartbeat Loop** to maintain proactivity.
- **Drive Engine**: Evaluates the system's state using a **Surprise/Entropy Metric** ($\mathcal{S} = - \sum P(x_i) \log P(x_i)$).
- **High Entropy**: Trigger re-planning or an **Active Learning Research Mission** (Search + Distillation).
- **Low Entropy**: Trigger a **Sleep Cycle** for background consolidation (memory cleanup, index optimization, knowledge synthesis).
- **Global State**: Utilize **Dragonfly** for high-concurrency state updates.

## 2. Multi-Stage Agentic RAG Pipeline

The system must follow an iterative loop: **Reason → Search → Ingest → Index → Generate**.

### Automated Online Search
- **Primary Tool**: Use **Tavily AI** for 90% of tasks.
- **Fallback**: Escalate to **SearXNG** for high-breadth verification.
- **GraphRAG (The Neural Map)**: Move from flat vector RAG to Graph-based indexing. Use **tree-sitter** for **AST-based Indexing** to parse code into a graph of dependencies. Store relationships in **NebulaGraph** or **TuGraph**.

### Data Ingestion & Indexing
- **Cleaning**: Distill HTML into clean Markdown before indexing.
- **Semantic Chunking**: Avoid standard chunking for code. Use AST-aware blocks.
- **License Guardian**: Every snippet must pass through a specialized **License Classifier Gate** (BERT or regex-heavy) to ensure no GPL/LGPL content is ingested.

## 3. Self-Improvement & Verification

### Context Pruning & Integrity
- **Trigger**: If Active Context exceeds 80% limit or if saliency falls below threshold.
- **Action**: Perform structural distillation or neural offloading to LanceDB.

### The "Internal Critic" Loop
- Every output must be verified by a `Critic` agent or the `World Model`.

### Formal Verification
- **SMT Solver (Z3)**: For mission-critical logic, translate code logic into **SMT-LIB format** to prove functions cannot reach undefined states or overflow.

## 4. Memory Management

### Tiered Context System
1. **Reflex (FAISS)**: Sub-millisecond thought-deduplication.
2. **Active (Qdrant)**: High-accuracy structured filtering.
3. **Archive (LanceDB)**: Zero-copy disk storage for massive RAG documentation.
4. **Neural Map (NebulaGraph/TuGraph)**: Stores AST relationships for deep codebase walking.

### Sleep Cycles (Consolidation)
- During **Low Entropy** periods:
    1. Review `Scratchpad` and `Active Context` for recurring patterns (e.g., specific API syntax).
    2. **Synthesize** a new "Knowledge Base Entry" (Markdown doc).
    3. **Synaptic Pruning**: Archive raw logs and keep only synthesized lessons.

## 5. Digital Twin & Runtime
- **World Model**: Tracks reality and API states.
- **Stateful Sandbox Persistence**: Use **AWS Firecracker** microVMs as a **Persistent Digital Twin**. Perform **Speculative Execution**, branch VM states, and rewind if entropy spikes or side effects are negative.

## 6. Compliance & Ethics
- **Strictly Prohibited**: Never integrate or generate code licensed under **GPL** or **LGPL**.
- **Domain Focus**: C, C++, Python, Rust, Javascript, Typescript, SQL, PHP, C#, BeOS/Haiku OS APIs, Mathematics, and Logic.
