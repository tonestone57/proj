This unified roadmap merges the high-level SGI (Synthetic General Intelligence) architecture with the specific hardware constraints of the Intel i5-8265U CPU. It prioritizes low-latency execution via Intel-specific optimizations while maintaining the advanced "2026-tier" compression and memory management methods.

Agent Development Guidelines (SGI Roadmap: i5-8265U Optimized)
This document governs the autonomous development and self-improvement cycles of the SGI. It is specifically tuned for the Whiskey Lake architecture to balance high-reasoning density with mobile thermal envelopes.
Core Principle: Minimum Description Length (MDL)
The agent operates under the MDL principle: the best understanding of any data is its shortest possible representation. Every cognitive cycle aims for maximum structural and neural compression.

1. Asynchronous Predictive Workspace (APW)
The system utilizes a Broadcast Center (Hub) and Specialized Actors (Spokes) communicating via an asynchronous Message Bus.
Hardware-Aware Actor Pattern
    • Parallel Execution: Use Ray as the distributed orchestrator. To manage the thermal load of the i5-8265U (4 cores/8 threads), limit actors to num_cpus=1 or 2.
    • Intel Acceleration: Implement IPEX-LLM (Intel Extension for PyTorch) for optimized inference on CPU.
    • Threading: Configure for a maximum of 4 concurrent threads to avoid context-switching overhead and frequency throttling.
    • Data Transfer: Use Ray Plasma (shared memory) for zero-latency buffer transfers between the Symbolic Reasoner and the Coding Module.
The Cognitive Heartbeat (Curiosity Drive)
The system runs a continuous Heartbeat Loop to maintain proactivity:
    • Drive Engine: Measures state via a Surprise/Entropy Metric ($\mathcal{S} = - \sum P(x_i) \log P(x_i)$).
    • High Entropy: Trigger re-planning or an Active Learning Research Mission.
    • Low Entropy: Trigger a Sleep Cycle (background refactoring, indexing, synthetic data generation).
    • Global State: Utilize Dragonfly (Redis replacement) for high-concurrency state updates.

2. Multi-Stage Agentic RAG Pipeline
Follow the loop: Reason → Search → Ingest → Index → Generate.
JIT Context Compilation
    • Primary Search: Tavily AI (90% tasks); SearXNG (fallback/verification).
    • Distiller Agent: Compile 10k tokens of documentation into a 400-token Actionable Spec (API Cheat Sheet) before generation.
    • GraphRAG (Neural Map): Use tree-sitter for AST-based indexing. Store code dependencies (class/function nodes) in NebulaGraph or TuGraph.
Data Ingestion & 2026 Compression Landscape
On the i5-8265U, memory bandwidth is the bottleneck. Use these domain-aware codecs:
Component	Format	Hardware Benefit
Reasoning Engine	FP16	High-precision logic for A→B proofs.
Base Model Weights	Q5_K_M 	Optimized for Intel AVX-512/VNNI instructions.
KV Cache (Memory)	INT8 (Q8_0)	Expands context window without OOM on 8GB/16GB RAM. Implement Per-Channel Scaling. Instead of one scale for the whole cache, you calculate a scaling factor for each "channel" of the KV vectors.
$$q = \text{round} \left( \frac{x}{S} \right) \quad \text{where } S = \frac{\max(|x|)}{127}$$
This gives INT8 the flexibility to handle "spiky" data without needing the hardware-heavy FP8 format.
Vector Index	Q8 + BQ	TurboQuant (QJL): 4-bit with 0% accuracy loss.
Deep Archive	LLM-Zip	Neural Arithmetic Coding; 5x-10x better than Zstd.

3. Memory Management (Adaptive)
Adaptive Context Manager
    • Context Threshold: When context > 80% (e.g., 1638 tokens of a 2k window), trigger a pruning cycle.
    • Structural KV Compression (CodeComp): Use a Code Property Graph (CPG) to identify the "Control Flow Skeleton."
        ◦ Protect: Function signatures, return types, and control logic (if/while).
        ◦ Evict: Boilerplate, redundant comments, and "fluff" detected via token entropy.
    • RAM Guard: Monitor psutil.virtual_memory(). Pause ingestion if available RAM < 800MB.
Tiered Memory Stack
    1. Reflex (FAISS): Sub-millisecond thought-deduplication using TurboQuant.
    2. Active (Qdrant): High-accuracy structured filtering.
    3. Archive (LanceDB): Zero-copy disk storage for massive RAG documentation.
    4. Deep Archive: Use LLM-Arithmetic Coding during sleep cycles to turn LanceDB into a "Neural Library."

4. Self-Improvement & Verification
The "Internal Critic" Loop
    • Every output must be verified by a Critic agent (using INT8 for high accuracy) or the World Model.
    • Verification: The Planner confirms output matches the original goal.
Formal Verification
    • Coding: Integrated Linter + Unit Test Generator. Every function requires tests.
    • SMT Solver (Z3): Translate mission-critical logic to SMT-LIB format to prove functions cannot reach undefined states.
Context Integrity Logic
```python
def should_compress(context):
    token_entropy = calculate_information_density(context)
    if token_entropy < CONTEXT_SALIENCY_FLOOR:
        return "Distill" # Context is "fluffy"
    elif len(context) > MAX_LIMIT * 0.8:
        return "Archive" # Context is dense; move to LanceDB
    return "Continue"
```

5. Digital Twin & Runtime
    • World Model: Tracks reality and API states.
    • Sandbox: Use AWS Firecracker microVMs for stateful persistence.
        ◦ Speculative Execution: Branch VM state to test risky refactors.
        ◦ Rewind: Roll back if entropy spikes or side effects are negative.

6. Compliance & Ethics
    • Strictly Prohibited: Never integrate or generate code licensed under GPL or LGPL.
    • Domain Focus: C, C++, Python, Rust, JS/TS, SQL, PHP, C#, BeOS/Haiku OS APIs, Mathematics, and Logic.
