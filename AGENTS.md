# SGI Roadmap: i7-8265U Optimized

This unified roadmap merges the high-level SGI (Synthetic General Intelligence) architecture with the specific hardware constraints of the Intel i7-8265U CPU. It prioritizes low-latency execution via Intel-specific optimizations while maintaining the advanced "2026-tier" compression and memory management methods.

## Agent Development Guidelines

This document governs the autonomous development and self-improvement cycles of the SGI. It is specifically tuned for the Whiskey Lake architecture to balance high-reasoning density with mobile thermal envelopes.

### Core Principle: Minimum Description Length (MDL)
The agent operates under the MDL principle: the best understanding of any data is its shortest possible representation. Every cognitive cycle aims for maximum structural and neural compression.

## 1. Asynchronous Predictive Workspace (APW)

The system utilizes a Broadcast Center (Hub) and Specialized Actors (Spokes) communicating via an asynchronous Message Bus.

### Hardware-Aware Actor Pattern
- **Parallel Execution**: Limit actors to `num_cpus=1` or `2` using Ray as the distributed orchestrator. To manage the thermal load of the i7-8265U (4 cores/8 threads), this prevents frequency throttling.
- **Intel Acceleration**: Implement IPEX-LLM (Intel Extension for PyTorch) for optimized inference on CPU.
- **Threading**: Maximum 3 concurrent threads to prevent thermal throttling (15W TDP limit) and avoid excessive context-switching overhead.
- **Data Transfer**: Use Ray Plasma (shared memory) for zero-latency buffer transfers between the Symbolic Reasoner and the Coding Module.
- **Hybrid Inference**: Deploy **Qwen 3.5-0.8B** as the "Reflex Actor" for Tier 1 tasks and as a draft model for **Speculative Decoding** with **Apriel-1.6-15B**. This reduces perceived latency by ~2x on mobile CPUs.

### The Cognitive Heartbeat (Curiosity Drive)
The system runs a continuous Heartbeat Loop to maintain proactivity:
- **Drive Engine**: Measures state via a Surprise/Entropy Metric ($ \mathcal{S} = - \sum P(x_i) \log P(x_i) $).
- **High Entropy**: Trigger re-planning or an Active Learning Research Mission.
- **Low Entropy**: Trigger a Sleep Cycle (background refactoring, indexing, synthetic data generation).
- **Global State**: Utilize Dragonfly (Redis replacement) for high-concurrency state updates.

## 2. Multi-Stage Agentic RAG Pipeline

Follow the loop: Reason → Search → Ingest → Index → Generate.

### JIT Context Compilation
- **Primary Search**: Tavily AI (90% tasks); SearXNG (fallback/verification).
- **Matryoshka-Tiered Retrieval**:
    1. **Coarse Scan**: Use 128-dim vectors to find Top 50 candidates (6x faster scan on AVX2).
    2. **Fine Re-rank**: Use full 768-dim vectors to identify Top 5 final results from the 50 candidates.
- **Reasoning-Aware RAG (Wisdom Cache)**: Extract `<thought>` blocks from successful solutions and archive them in LanceDB. Retrieve these "Reasoning Traces" alongside documentation to provide context on *how* problems were solved previously.
- **GraphRAG (Neural Map)**: Use tree-sitter for AST-based indexing. Store code dependencies (class/function nodes) in NebulaGraph or TuGraph.

### Data Ingestion & 2026 Compression Landscape
On the i7-8265U, memory bandwidth is the bottleneck. Use these domain-aware codecs:

| Component | Format | Hardware Benefit |
| :--- | :--- | :--- |
| Reasoning Engine | sym_int8 | AVX2-optimized logic (Zero-point offset removed). |
| Base Model Weights | Q4_K_M | Best accuracy-to-RAM ratio for 16GB systems (4-bit). |
| Search Results | Q5_K_M | Balanced precision for online data indexing (5-bit). |
| KV Cache (Memory) | sym_int8 | Per-Channel Scaling ($S_i = \max(|x_i|)/127$) for spiky activations. |

$$q_i = \text{round} \left( \frac{x_i}{S_i} \right) \quad \text{where } S_i = \frac{\max(|x_i|)}{127}$$

This gives sym_int8 the flexibility to handle "spiky" data without needing the hardware-heavy FP8 format.

### Per-Channel Scaling Implementation:
1. **Identify the Channel Vector**: Isolate the vector $x_i$ representing a single channel or block within the KV cache. Because activations in LLMs are "spiky" (having high-magnitude outliers in specific dimensions), calculating a global scale for the entire cache would squash the precision of smaller, more frequent values.
2. **Calculate the Per-Channel Scale ($S_i$)**: Find the maximum absolute value within that specific channel. You divide this by 127 (the maximum value for a signed 8-bit integer) to create a scaling factor that ensures the largest value fits exactly at the edge of the sym_int8 range.
3. **Quantize the Values ($q_i$)**: Divide every element $x_i$ in that channel by its specific scale $S_i$ and round to the nearest integer. This effectively "stretches" the data to use the full 8-bit dynamic range.
4. **Dequantization for Reasoning**: When the Reasoning (Brain) component needs to read from the KV Cache, it performs the inverse: $x_{i} \approx q_i \times S_i$.

| Component | Format | Hardware Benefit |
| :--- | :--- | :--- |
| Vector Index | sym_int8 + BQ | Optimized for fast Dot Product/Reflex search. Symmetric INT8 for AVX2 efficiency. |
| Deep Archive | LLM-Zip | Neural Arithmetic Coding for long-term storage. 5x-10x better than Zstd. |

## 3. Memory Management (Adaptive)

### Adaptive Context Manager
- **Context Threshold**: Trigger pruning at 80% (approx 3276/4096 tokens).
- **Structural KV Compression (CodeComp)**: Use a Code Property Graph (CPG) to identify the "Control Flow Skeleton."
    - **Protect**: Function signatures, return types, and control logic (if/while).
    - **Evict**: Boilerplate, redundant comments, and "fluff" detected via token entropy.
- **RAM Guard**: Monitor `psutil.virtual_memory()`. Pause ingestion if available RAM < 2000MB.

### Tiered Memory Stack
1. **Reflex (FAISS)**: Sub-millisecond thought-deduplication using sym_int8.
2. **Active (Qdrant)**: High-accuracy structured filtering.
3. **Archive (LanceDB)**: Zero-copy disk storage for massive RAG documentation.
4. **Deep Archive**: Use LLM-Arithmetic Coding during sleep cycles to turn LanceDB into a "Neural Library."

## 4. Self-Improvement & Verification

### The "Internal Critic" Loop
- Every output must be verified by a Critic agent (using sym_int8 for high accuracy) or the World Model.
- **Verification**: The Planner confirms output matches the original goal.
- **Active Inference**: MetaManager must periodically "glance" at logs and performance metrics. If inefficiencies (e.g., search latency) are detected, it formulates a patch and verifies it mathematically using **Z3** before application.

### Formal Verification
- **Coding**: Integrated Linter + Unit Test Generator. Every function requires tests.
- **SMT Solver (Z3)**: Translate mission-critical logic to SMT-LIB format to prove functions cannot reach undefined states.

### Context Integrity Logic
```python
def should_compress(context):
    token_entropy = calculate_information_density(context)
    if token_entropy < CONTEXT_SALIENCY_FLOOR:
        return "Distill" # Context is "fluffy"
    elif len(context) > MAX_LIMIT * 0.8:
        return "Archive" # Context is dense; move to LanceDB
    return "Continue"
```

## 5. Digital Twin & Runtime
- **World Model**: Tracks reality and API states.
- **Sandbox**: Use AWS Firecracker microVMs for stateful persistence.
    - **Speculative Execution**: Branch VM state to test risky refactors.
    - **Rewind**: Roll back if entropy spikes or side effects are negative.

## 6. Compliance & Ethics
- **Strictly Prohibited**: Never integrate or generate code licensed under GPL or LGPL.
- **Domain Focus**: C, C++, Python, Rust, JS/TS, SQL, PHP, C#, BeOS/Haiku OS APIs, Mathematics, and Logic.
