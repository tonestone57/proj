# Agent Development Guidelines (SGI Roadmap)

This file provides instructions for the AGI (or Synthetic General Intelligence - SGI) to follow during its autonomous development and self-improvement cycles.

## 1. Asynchronous Predictive Workspace (APW)

The system operates as a central **Broadcast Center** (Hub) with **Specialized Actors** (Spokes) communicating over an asynchronous **Message Bus**.

### The Actor Pattern
- Modules must work in parallel. The Hub broadcasts a goal, and multiple actors (e.g., Symbolic Reasoner, Coding Module) work simultaneously. The Hub selects the best result.

### The Cognitive Heartbeat
- The system runs a **Heartbeat Loop** to maintain proactivity.
- **Drive Engine**: Evaluates the system's state using a **Surprise/Entropy Metric** ($\mathcal{S} = - \sum P(x_i) \log P(x_i)$).
- **High Entropy**: Trigger re-planning.
- **Low Entropy**: Trigger background consolidation (memory cleanup, index optimization).

## 2. Multi-Stage Agentic RAG Pipeline

The system must follow an iterative loop: **Reason → Search → Ingest → Index → Generate**.

### Automated Online Search
- **Primary Tool**: Use **Tavily AI** or **SearXNG** for high-relevance, LLM-optimized search results.
- **Search Strategy**: Employ **Multi-Perspective Search**—query both the main thesis and its antithesis to minimize bias.
- **Ethical Scraping**: Always check `robots.txt` and use libraries like `Crawl4AI` or `BeautifulSoup` to extract clean Markdown content.

### Data Ingestion & Indexing
- **Cleaning**: Distill HTML into clean Markdown before indexing.
- **Semantic Chunking**: Split data into 200–400 word blocks representing complete ideas.
- **Contextual Retrieval**: Attach a document summary to every chunk to preserve global context.
- **Vector Store**: Use **FAISS** for short-term/high-speed tasks and **LanceDB** for long-term/persistent knowledge storage.

## 3. Self-Improvement & Verification

### The "Internal Critic" Loop
- Every output from the `Symbolic Reasoner` or `Coding Module` must be verified by a `Critic` agent or the `World Model` before being finalized.
- **Verification Step**: The `Planner` must confirm the output matches the original goal.

### Formal Verification for Logic & Math
- **Coding**: Integrate a **Linter** and **Unit Test Generator**. Every generated function must be accompanied by its own tests.
- **Mathematics**: Force the use of Python or formal verification tools (Lean, WolframAlpha) for multi-step arithmetic or logic proofs.

## 4. Memory Management

### Tiered Context System
- **Active Context**: Last 2-3 turns of thought.
- **Compressed Context**: Summarized conversation history (handled by high-speed models).
- **Archived Context**: Vector embeddings in **LanceDB**.

### Working Memory (Scratchpad)
- Use the `Scratchpad Memory` in the `Global Workspace` for intermediate logical steps ($A \rightarrow B$). This prevents the context window from being cluttered with transient thoughts that don't need long-term indexing.

### Recursive Theory of Mind
- The `Social Module` must track not just what the user says, but the underlying intent and knowledge gaps (Recursive Theory of Mind).

## 5. Compliance & Ethics
- **Strictly Prohibited**: Never integrate or generate code licensed under **GPL** or **LGPL**.
- **Domain Focus**: Prioritize data and logic related to **C, C++, Python, Rust, Javascript, Typescript, SQL, PHP, C#, BeOS/Haiku OS APIs, Mathematics, and Logic**.
