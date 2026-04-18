# Agent Development Guidelines (SGI Roadmap)

This file provides instructions for the AGI (or Synthetic General Intelligence - SGI) to follow during its autonomous development and self-improvement cycles.

## 1. Asynchronous Predictive Workspace (APW)

The system operates as a central **Broadcast Center** (Hub) with **Specialized Actors** (Spokes) communicating over an asynchronous **Message Bus**.

### The Actor Pattern
- **Parallel Execution**: Modules operate as autonomous, concurrent units. The Hub broadcasts objectives to specialized actors (e.g., Symbolic Reasoner, Coding Module) and synthesizes the optimal response.
- **Implementation**: Utilize **Ray** as the primary distributed orchestrator. Actors must run in isolated processes to prevent CPU-heavy workloads from blocking the central Message Bus. Use **gRPC** specifically for low-latency interfacing with non-Python or external microservices.

### The Cognitive Heartbeat
- The system runs a **Heartbeat Loop** to maintain proactivity.
- **Drive Engine**: Evaluates the system's state using a **Surprise/Entropy Metric** ($\mathcal{S} = - \sum P(x_i) \log P(x_i)$).
- **High Entropy**: Trigger re-planning.
- **Low Entropy**: Trigger background consolidation (memory cleanup, index optimization, sleep cycles).
- **Global State**: Utilize **Dragonfly** (drop-in Redis replacement) for high-concurrency state updates.

## 2. Multi-Stage Agentic RAG Pipeline

The system must follow an iterative loop: **Reason → Search → Ingest → Index → Generate**.

### Automated Online Search
- **Primary Tool**: Use **Tavily AI** for 90% of tasks (low-latency, structured reasoning).
- **Fallback**: Escalate to **SearXNG** for high-breadth, multi-engine verification during Low-Entropy cycles.
- **Search Strategy**: Employ **Multi-Perspective Search**—query both the main thesis and its antithesis to minimize bias.
- **Ethical Scraping**: Always check `robots.txt` and use libraries like `Crawl4AI` or `BeautifulSoup` to extract clean Markdown content.
- **GraphRAG (The Neural Map)**: Move from flat vector RAG to Graph-based indexing. Use `tree-sitter` for AST-based indexing and store relationships in NebulaGraph/TuGraph.

### Data Ingestion & Indexing
- **Cleaning**: Distill HTML into clean Markdown before indexing.
- **Semantic Chunking**: Split data into 200–400 word blocks representing complete ideas.
- **Contextual Retrieval**: Attach a document summary to every chunk to preserve global context.
- **Vector Store**: Use **FAISS** for short-term/high-speed tasks and **LanceDB** for long-term/persistent knowledge storage.
- **License Guardian**: Every snippet must pass through a `License_Actor` to ensure no GPL/LGPL content is ingested.

## 3. Self-Improvement & Verification

### Context Pruning & Integrity
- **Trigger**: If Active Context exceeds 80% of the maximum token limit, OR if `token_entropy` falls below `CONTEXT_SALIENCY_FLOOR`.
- **Action**:
    - **Distill**: If entropy is low ("fluff"), perform structural distillation (AST-aware KV pruning).
    - **Archive**: If context is dense but full, perform neural offloading to LanceDB.

### The "Internal Critic" Loop
- Every output from the `Symbolic Reasoner` or `Coding Module` must be verified by a `Critic` agent or the `World Model` before being finalized.
- **Verification Step**: The `Planner` must confirm the output matches the original goal.

### Formal Verification for Logic & Math
- **Coding**: Integrate a **Linter** and **Unit Test Generator**. Every generated function must be accompanied by its own tests.
- **SMT Solver (Z3)**: Use symbolic reasoning to prove that critical logic (e.g., memory management) cannot reach undefined states.

## 4. Memory Management

### Tiered Context System
- **Active Context**: Last 5 turns of thought.
- **Compressed Context**: Summarized conversation history (handled by high-speed models).
- **Archived Context**: Vector embeddings in **LanceDB**. Use **LLM-Arithmetic Coding** for lossless neural archiving of deep sessions.
- **Working Memory**: Use **Ray Plasma** (shared memory) for zero-latency data passing between actors.

### "Gold Standard" Tiered Memory Stack
1. **Reflex (FAISS)**: Embedded in the Workspace for sub-millisecond thought-deduplication. Use **TurboQuant (QJL)** for 3-bit zero-loss compression.
2. **Active (Qdrant)**: High-accuracy structured filtering for the Social and Self modules.
3. **Archive (LanceDB)**: Zero-copy disk storage for massive RAG documentation and knowledge.

### Sleep Cycles
- During "Low Entropy" periods, trigger a sleep cycle for **Synaptic Pruning** and **Knowledge Synthesis**.

## 5. Digital Twin & Runtime
- **World Model**: Maintains a persistent representation of reality.
- **Stateful Sandbox**: Use **AWS Firecracker** microVMs as a persistent Digital Twin of the target system for speculative execution and side-effect observation.

## 6. Compliance & Ethics
- **Strictly Prohibited**: Never integrate or generate code licensed under **GPL** or **LGPL**.
- **Domain Focus**: Prioritize data and logic related to **C, C++, Python, Rust, Javascript, Typescript, SQL, PHP, C#, BeOS/Haiku OS APIs, Mathematics, and Logic**.
