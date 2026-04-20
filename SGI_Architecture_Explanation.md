# SGI-Alpha: LLM Integration & Autonomous Architecture Explanation

The **SGI-Alpha** (Synthetic General Intelligence) system is a modular architecture designed for high-level reasoning, coding, and logical processing, optimized for Intel hardware (specifically the i7-8265U).

## 1. Why the LLM Model is Loaded
The system loads a primary LLM (defaulting to **DeepSeek-Coder-V2-Lite**) as a **Shared Singleton** via the `ModelRegistry`.

*   **Memory Efficiency**: By loading the model once into shared memory (via Ray), the system prevents "RAM thrashing" on 16GB hardware.
*   **Specialized Quantization**: The model is loaded in **UD-Q5_K_M** precision using `ipex-llm`, allowing a 14B+ parameter model to run efficiently on a 15W TDP mobile CPU.
*   **Shared Intelligence**: It acts as the "Central Brain" that all specialized actors (Coding, Reasoning, Planning, Critic) call upon for semantic tasks.

## 2. Why it loads "another" Model (The Embedding Model)
In addition to the generative LLM (DeepSeek), the system loads a second, smaller model: **all-MiniLM-L6-v2**.

*   **What it is used for**: This is an **Embedding Model** used for the Vector Index (RAG).
*   **How it works**: It converts text (logs, code, documentation) into numerical vectors (embeddings) that are stored in **LanceDB**.
*   **Why both?**: The generative LLM is great at "thinking" and "writing," but it is too slow and computationally expensive to use for searching through millions of archived documents. The embedding model allows the system to perform sub-millisecond "semantic searches" to find relevant context before the generative LLM starts its reasoning process.

## 3. How the Models Work Together
The system uses a **Multi-Stage Agentic RAG Pipeline**:
1.  **Search/Retrieve**: The embedding model finds relevant facts in LanceDB.
2.  **Reason**: The Reasoner Actor uses the generative LLM to analyze the retrieved facts.
3.  **Plan**: The Planner Actor uses the LLM to decompose the goal into steps.
4.  **Execute**: The Coding Actor writes and tests code based on the plan.

## 4. Autonomy and Self-Improvement
SGI-Alpha is designed to operate without human intervention:

*   **Cognitive Heartbeat**: The `DriveEngine` calculates the system's **Entropy** (uncertainty).
    *   **High Entropy (Surprise)**: The system realizes it is facing a new problem and triggers the Planner to generate a new strategy.
    *   **Low Entropy (Boredom)**: The system enters a **"Sleep Cycle"** to autonomously refactor its own code, synthesize new knowledge base entries, and compress its memory archives.
*   **Meta-Learning**: The `MetaManager` monitors the performance of each module. If the Coding Actor's confidence score drops, the Meta-Learning engine autonomously adjusts its parameters or triggers a search for better documentation.
*   **Self-Correction**: The **Internal Critic** reviews the output of other actors. If it detects a logic violation (using semantic analysis or the Z3 SMT solver), it rejects the task and sends it back for re-planning.

## 5. Summary Table

| Component | Model / Technology | Function |
| :--- | :--- | :--- |
| **Generative Brain** | DeepSeek-Coder-V2-Lite | Reasoning, Coding, Planning |
| **Vector Search** | all-MiniLM-L6-v2 | RAG retrieval, Semantic indexing |
| **Quantization** | UD-Q5_K_M / sym_int8 | 2026-tier Intel AVX2 optimization |
| **Self-Improvement** | Meta-Learning / Sleep Cycles | Autonomous performance optimization |
| **Safety Gate** | License Guardian / Z3 | Prohibits GPL code and proves logic safety |

This architecture ensures that the system is not just "predicting the next token," but actively managing its resources, verifying its own logic, and improving its capabilities over time.
