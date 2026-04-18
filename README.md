# AGI LLM for Coding, Math and Logic

This repository contains a modular AGI (Artificial General Intelligence) architecture designed for high-level reasoning, mathematical evaluation, and logical processing.

## Architecture

The system utilizes an **Asynchronous Predictive Workspace (APW)**. Unlike traditional models, the Hub acts as a **Broadcast Center** using Pub/Sub logic to eliminate bottlenecks. It implements a **Multi-Stage Agentic RAG Pipeline** and is designed for **Self-Improvement**, autonomously updating its data files and logic to achieve better accuracy and reliability.

### The Dual-Stream System
To maximize performance, cognitive workload is split into two tracks:
- **The Reflex Arc (Fast Path):** Low-latency modules (Safety, Syntax Checking) that act instantly.
- **The Global Workspace (Slow Path):** Higher-order reasoning (Planning, Complex Coding) requiring full attention.

### Core Components
- **Message Bus (The Spine)**: An asynchronous bus where all modules post their state.
- **Integrator (The Hub)**: Samples the Message Bus every "Tick" to form a coherent global state.
- **Drive Engine (Drives Module)**: Calculates a **Surprise/Entropy Metric** to proactively trigger re-planning or background consolidation.
- **Internal Critic**: Verifies the logic and safety of outputs before they are finalized.
- **Scratchpad Memory**: A dedicated working memory area for intermediate reasoning steps.

### Dynamic Processing System (DPS)
- **Task Router**: Directs messages to the appropriate modules.
- **Priority Engine**: Computes dynamic priorities based on context and urgency.
- **Attention Gate**: Filters and amplifies signals to manage cognitive load. Integrates with the **Ethics** module for proactive vetting.

### Specialized Modules
- **Symbolic Reasoner**: Handles mathematical and logical queries.
- **Coding Module**: Executes and verifies Python code in a restricted sandbox.
- **Search Agent**: Performs autonomous online searches using APIs like Tavily to retrieve fresh information.
- **Critic**: Evaluates the reasoning of other modules to ensure accuracy and safety.
- **Vision Module**: Processes visual inputs.
- **Planner**: Generates step-by-step plans to achieve goals.
- **Self Model**: Tracks the AGI's internal state and identity.
- **World Model**: Maintains a persistent representation of reality, distinguishing between internal cognitive states and external environment states.
- **Social Module**: Inferred beliefs, intentions, and social interactions, integrated with **Episodic Memory** for user context.

---

## RAG & Knowledge Extraction (GGUF)

To expand the AGI's knowledge base beyond its core modules, the system supports **Retrieval-Augmented Generation (RAG)** by extracting data from **GGUF** models.

### Extraction Process
1. **Probe**: The GGUF model is prompted to generate exhaustive information on target topics.
2. **Embed**: Generated text is converted into mathematical vectors (embeddings).
3. **Compress**: Vectors are stored in optimized formats for high-speed retrieval.

### Storage Options
The AGI uses a tiered storage system to manage cognitive state and external knowledge:

| Feature | Semantic Cache | FAISS | LanceDB |
| :--- | :--- | :--- | :--- |
| **Type** | Sub-millisecond **Cache**. | Low-level **Library**. | Serverless **Database**. |
| **Primary Storage** | **In-Memory.** | **RAM-first.** | **Disk-first.** |
| **Persistence** | Volatile (Redis). | Manual `.index` files. | Automatic (SQLite-like). |
| **Compression** | Key-Value Pairs. | Product Quantization (PQ). | Columnar (Lance format). |
| **Use Case** | **Reflex Cache** & Latency Reduction. | **Short-term Memory** & **DPS**. | **Long-term Memory** & **World Model**. |

- **Semantic Cache**: Uses tools like `Redis` or `GPTCache` to store semantically identical thought processes, dropping response times to milliseconds.
- **FAISS**: Best for the **DPS** where microsecond latency is critical for comparing current "thoughts" against recent cognitive history.
- **LanceDB**: Best for the **World Model**, allowing the storage of terabytes of extracted knowledge on disk while supporting complex metadata filtering.

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
- **Formal Verification**: Integration with tools like Lean or WolframAlpha for rigorous proof checking.

### Coding & Self-Improvement
The `CodingModule` executes code across supported languages and specialized APIs, operating as a **Specialized Actor** in parallel with other modules.
- **Polyglot Execution**: Sandboxed execution and testing for C, C++, Python, Rust, Javascript, Typescript, SQL, PHP, and C#.
- **Execution Environment**: Compiled languages are tested inside ultra-lightweight microVMs (e.g., **AWS Firecracker**) or compiled to **WebAssembly (WASM)** for near-instant, secure execution.
- **Specialized APIs**: Deep integration with **BeOS** and **Haiku OS** APIs.
- **Cognitive Heartbeat**: Runs a proactive loop that triggers internal verification and optimization tasks without user input.
- **Autonomous Verification**: Proactively writes unit tests and runs background checks to find and fix edge-case errors.
- **Autonomous Research**: The system can search online to find latest libraries, fix bugs, or learn new algorithms.

## Directory Structure

```text
├── core/
│   ├── message_bus/       # Pub/Sub event router (Redis/ZeroMQ)
│   ├── heartbeat.py       # The autonomous cognitive loop
│   └── drives.py          # Entropy/Surprise calculator
├── actors/                # Formerly 'modules' - Independent processes
│   ├── coding_actor.py    # Polyglot sandbox execution
│   ├── reasoner_actor.py  # Lean/Wolfram integration
│   ├── search_actor.py    # Tavily/Crawl4AI RAG loop
│   └── critic_actor.py    # Output verification
├── memory/
│   ├── cache/             # Sub-millisecond Semantic Cache
│   ├── short_term/        # FAISS (Active Context)
│   ├── long_term/         # LanceDB (Archived Context)
│   └── scratchpad.py      # Transient reasoning steps
├── world_model/           # External reality and API state tracking
└── safety_ethics/         # License compliance (No GPL) and alignment
```

---

## Licensing and Compliance

**Strict Requirement**: This repository and all associated data files must NOT contain any code licensed under **GPL** or **LGPL**. All contributions and indexed data must adhere to permissive licenses (e.g., MIT, Apache 2.0, BSD) or be original works.
