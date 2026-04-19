# SGI-Alpha: Asynchronous Predictive Workspace for Intel i5-8265U

This repository implements a modular SGI (Synthetic General Intelligence) architecture optimized for the **Intel Core i5-8265U** platform using **2026 Compression Standards**.

## Philosophical Foundation: Minimum Description Length (MDL)
The system operates under the MDL principle: the best understanding of any data is its shortest possible representation. Every cognitive cycle aims for maximum structural and neural compression.

## Architecture: Asynchronous Predictive Workspace (APW)
The system uses a **Broadcast Center (SGIHub)** and specialized **Ray Actors** communicating over an asynchronous message bus.

### Core Components
- **Global Workspace**: Distributed state management via Ray.
- **Scheduler**: Priority-based task orchestration.
- **Drive Engine**: Entropy-driven proactive mission triggering.
- **Thermal Guard**: Real-time CPU monitoring (78°C limit) for 15W TDP stability.

### Specialized Actors
- **CodingActor**: NF4 precision, speculative execution (Firecracker VMs), and AST-aware distillation.
- **ReasonerActor**: BF16 precision, Z3 SMT-LIB formal verification.
- **SearchActor**: JIT Context Compilation and License Guardian (No GPL).
- **InternalCritic**: Pre-finalization output verification.
- **MemoryManager**: 2026 Tiered Memory Stack (TurboQuant, LLM-Zip, AST Serialization).

## 2026 Compression Standards (Domain-Aware)

| Track | 2026 Standard | SGI Implementation |
| :--- | :--- | :--- |
| **Reasoning Engine** | **BF16 (Q16)** | Maximum logic fidelity. |
| **Model Weights** | **NF4** | 4-bit NormalFloat for CPU efficiency. |
| **Vector Index/RAG** | **Q8 + Binary Quantization** | TurboQuant (PolarQuant + QJL). |
| **KV Cache (Memory)** | **FP8 (E4M3)** | High dynamic range for activations. |
| **Search/Text Logs** | **Zstd-19** | Industry-standard log compression. |
| **Code Structure** | **AST Serialization** | Tree-sitter node operations. |

## Getting Started

Initialize the environment:
```bash
source setup_8265u.sh
```

Run the SGI:
```bash
python3 main.py
```

## Compliance
**Strict Requirement**: No code licensed under **GPL**, **LGPL**, or **AGPL** is permitted. The **License Guardian** enforces this gate during ingestion.
