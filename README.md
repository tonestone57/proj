# AGI LLM for Coding, Math and Logic

This repository contains a modular AGI (Artificial General Intelligence) architecture designed for high-level reasoning, mathematical evaluation, and logical processing.

## Architecture

The system follows a hub-and-spoke model with a **Global Workspace** and a **Dynamic Processing System (DPS)** orchestrating various specialized cognitive modules.

### Core Components
- **Global Workspace**: The central communication hub for all modules.
- **Scheduler**: Manages task execution based on dynamic priorities.
- **Autonomous Loop**: The main cognitive cycle that drives perception, reasoning, and action.

### Dynamic Processing System (DPS)
- **Task Router**: Directs messages to the appropriate modules.
- **Priority Engine**: Computes dynamic priorities based on context and urgency.
- **Attention Gate**: Filters and amplifies signals to manage cognitive load. Integrates with the **Ethics** module for proactive vetting.

### Specialized Modules
- **Symbolic Reasoner**: Handles mathematical and logical queries.
- **Coding Module**: Executes and verifies Python code in a restricted sandbox.
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
The AGI uses two primary vector storage engines depending on the required latency and scale:

| Feature | FAISS (Facebook AI Similarity Search) | LanceDB |
| :--- | :--- | :--- |
| **Type** | Low-level **Library**. | Serverless **Database**. |
| **Primary Storage** | **RAM-first.** | **Disk-first.** |
| **Persistence** | Manual `.index` files. | Automatic (SQLite-like). |
| **Compression** | Product Quantization (PQ). | Columnar (Lance format). |
| **Use Case** | **Short-term Memory** & **DPS**. | **Long-term Memory** & **World Model**. |

- **FAISS**: Best for the **DPS** where microsecond latency is critical for comparing current "thoughts" against recent cognitive history.
- **LanceDB**: Best for the **World Model**, allowing the storage of terabytes of extracted knowledge on disk while supporting complex metadata filtering.

---

## Getting Started

To run the AGI system:

```bash
python3 main.py
```

## Capabilities

### Mathematics and Logic
The `SymbolicReasoner` module evaluates complex expressions:
- **Arithmetic**: `math.factorial(5)`, `math.sqrt(16)`
- **Logic**: `True and (False or True)`

### Coding & Self-Correction
The `CodingModule` executes Python code. If an error occurs, the `Autonomous Loop` can route the failure back to the reasoning modules for correction.

## Directory Structure

- `core/`: Fundamental infrastructure.
- `dps/`: Executive control systems (Router, Attention Gate).
- `modules/`: Specialized cognitive modules (Coding, Social, Reasoning).
- `world_model/`: Internal reality mapping.
- `ethics/`, `safety/`: Alignment and risk management.
- `memory/`: Episodic and Semantic memory systems.
