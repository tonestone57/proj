# Agent Development Guidelines (SGI Roadmap)

This file provides instructions for the AGI (or Synthetic General Intelligence - SGI) to follow during its autonomous development and self-improvement cycles.

### Core Principle: Minimum Description Length (MDL)
The agent operates under the **MDL principle**: the best understanding of any data is its shortest possible representation. Every cognitive cycle should aim for maximum structural and neural compression.

## 1. Asynchronous Predictive Workspace (APW)

The system operates as a central **Broadcast Center** (Hub) with **Specialized Actors** (Spokes) communicating over an asynchronous **Message Bus**.

### The Actor Pattern
- **Parallel Execution**: Modules operate as autonomous, concurrent units in isolated processes. The Hub broadcasts objectives to specialized actors (e.g., Symbolic Reasoner, Coding Module) and synthesizes the optimal response.
- **Implementation**: Utilize **Ray** as the primary distributed orchestrator to bypass the Python GIL. Use **gRPC** specifically for low-latency interfacing with non-Python or external microservices.
- **Data Transfer**: Use **Ray Plasma** (shared memory object store) for zero-latency transfer of large technical data buffers between actors.

### The Cognitive Heartbeat (Curiosity Drive)
- The system runs a **Heartbeat Loop** to maintain proactivity.
- **Drive Engine**: Evaluates the system's state using a **Surprise/Entropy Metric** ($\mathcal{S} = - \sum P(x_i) \log P(x_i)$).
- **High Entropy**: Trigger re-planning or an **Active Learning Research Mission** (Documentation + Issue Tracker + Comparative Examples).
- **Low Entropy**: Trigger a **Sleep Cycle** for background consolidation (Refactoring, Indexing, Synthetic Data Gen).
- **Global State**: Utilize **Dragonfly** (drop-in Redis replacement) for high-concurrency state updates.

#### Conceptual Heartbeat Logic
```python
def heartbeat_tick():
    state = message_bus.get_current_state()
    entropy = calculate_entropy(state)

    if entropy > THRESHOLD_REPLAN:
        # High uncertainty: The agent is "confused" or facing a new problem
        planner.generate_new_strategy(reason="High System Entropy")
    elif entropy < THRESHOLD_CONSOLIDATE:
        # Low uncertainty: The agent is "bored"
        memory_manager.trigger_sleep_cycle()

    drives.update_objective_priorities()
```

## 2. Multi-Stage Agentic RAG Pipeline

The system must follow an iterative loop: **Reason → Search → Ingest → Index → Generate**.

### Automated Online Search
- **Primary Tool**: Use **Tavily AI** for 90% of tasks (low-latency, structured reasoning).
- **Fallback**: Escalate to **SearXNG** for high-breadth verification during background consolidation.
- **JIT Context Compilation**: Move from "Retrieved Chunks" to "Synthesized Micro-Contexts."
    - **Action**: Have a "Distiller" agent compile multiple documents into a single, high-density **Actionable Spec**.
    - **Goal**: Reduce 10,000 tokens of documentation to a 400-token "API Cheat Sheet" that captures exact syntax for the target system.
- **GraphRAG (The Neural Map)**: Use **tree-sitter** for **AST-based Indexing** to parse code into a graph of dependencies (classes/functions as nodes, calls as edges). Store relationships in **NebulaGraph** or **TuGraph**.
- **Search Strategy**: Employ **Multi-Perspective Search**—query both the main thesis and its antithesis to minimize bias.
- **Ethical Scraping**: Always check `robots.txt` and use libraries like `Crawl4AI` or `BeautifulSoup` to extract clean Markdown content.

### Data Ingestion & Indexing
- **Cleaning**: Distill HTML into clean Markdown before indexing.
- **Semantic Chunking**: Avoid standard chunking (200–400 words) for code, as it is the "death of context." Use **AST-aware blocks** to preserve structural relationships and non-linear dependencies.
- **Contextual Retrieval**: Attach a document summary to every chunk to preserve global context.
- **Vector Store**: Use **FAISS** for short-term/high-speed tasks and **LanceDB** for long-term/persistent knowledge storage.
- **Entropy-Targeted Quantization (TurboQuant)**:
    - **High Entropy Data**: Store at **FP16** or **INT8**.
    - **Low Entropy Data**: Store at **2-bit (Quantized Johnson-Lindenstrauss)**.
- **License Guardian**: Every snippet must pass through a specialized **License Classifier Gate**.

## 3. Self-Improvement & Verification

### Context Integrity Check
Refine the Context Pruning trigger from a simple "80% limit" to a **Context Integrity Check**:

```python
def should_compress(context):
    # Instead of just len(context) > threshold:
    token_entropy = calculate_information_density(context)
    if token_entropy < CONTEXT_SALIENCY_FLOOR:
        # The context is full of "fluff"; trigger structural distillation
        return "Distill"
    elif len(context) > MAX_LIMIT * 0.8:
        # The context is actually dense; trigger neural offloading to LanceDB
        return "Archive"
    return "Continue"
```

### Structural KV Cache Compression (CodeComp)
Instead of pruning by recency, use a **Code Property Graph (CPG)** to identify the "Control Flow Skeleton."
- **Action**: Calculate a **Structural Importance Score ($I_{struct}$)** for every token.
- **Protected Tokens**: Tokens representing function signatures, return types, and control logic (if/while) are protected.
- **Boilerplate Eviction**: Tokens representing boilerplate or redundant comments are evicted first.
- **Class Hierarchy Preservation**: For object-oriented APIs (like BeOS/Haiku), always retain `virtual` function overrides during distillation to preserve the code schema.

### The "Internal Critic" Loop
- Every output from the `Symbolic Reasoner` or `Coding Module` must be verified by a `Critic` agent or the `World Model` before being finalized.
- **Verification Step**: The `Planner` must confirm the output matches the original goal.

### Formal Verification
- **Coding**: Integrate a **Linter** and **Unit Test Generator**. Every generated function must be accompanied by its own tests.
- **SMT Solver (Z3)**: For mission-critical logic, translate code logic into **SMT-LIB format** to prove functions cannot reach undefined states or overflow.

## 4. Memory Management

### Tiered Context System
- **Active Context**: Last 5 turns of thought.
- **Compressed Context**: Summarized conversation history (handled by high-speed models).
- **Archived Context**: Vector embeddings in **LanceDB**. Use **LLM-Arithmetic Coding** for lossless neural archiving of deep sessions.
- **Working Memory**: Use **Ray Plasma** (shared memory) for zero-latency data passing between actors.

### "Gold Standard" Tiered Memory Stack
1. **Reflex (FAISS)**: Sub-millisecond thought-deduplication using **TurboQuant** (QJL).
2. **Active (Qdrant)**: High-accuracy structured filtering for the Social and Self modules.
3. **Archive (LanceDB)**: Zero-copy disk storage for massive RAG documentation.
4. **Neural Map (NebulaGraph/TuGraph)**: Stores AST relationships.

### Lossless Neural Archiving (LLM-Zip)
- **Neural Compression**: Use the system's reasoning capabilities to encode conversation history into dense, non-human-readable representations using **arithmetic coding** via LLM probabilities.
- **0% Information Loss**: When the agent needs to "remember" a deep session, it decompresses the neural representation back into the original token stream, bypassing the limits of natural language summarization.

### Sleep Cycles (Consolidation)
- During **Low Entropy** periods:
    1. Review `Scratchpad` and `Active Context` for patterns.
    2. **Synthesize** a new "Knowledge Base Entry."
    3. **Synaptic Pruning**: Archive raw logs and keep only synthesized lessons.

## 5. Digital Twin & Runtime
- **World Model**: Tracks reality and API states.
- **Stateful Sandbox Persistence**: Use **AWS Firecracker** microVMs as a **Persistent Digital Twin**.
    - **Speculative Execution**: Branch the VM state to try risky refactors.
    - **Observation**: Observe side effects on the "World" (system resources, logs, network calls).
    - **Rewind**: Roll back the state if entropy spikes or side effects are negative.

## 6. Compliance & Ethics
- **Strictly Prohibited**: Never integrate or generate code licensed under **GPL** or **LGPL**.
- **Domain Focus**: C, C++, Python, Rust, Javascript, Typescript, SQL, PHP, C#, BeOS/Haiku OS APIs, Mathematics, and Logic.
