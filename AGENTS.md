# SGI Development Guidelines (2026 Standards)

This repository follows the 2026 SGI roadmap for autonomous development and self-improvement.

## 1. APW Actor Pattern
- Use **Ray** for all distributed modules to bypass the Python GIL.
- All actors must inherit from `CognitiveModule`.
- Communication is asynchronous: actors broadcast results to the `GlobalWorkspace` via `self.workspace.broadcast.remote()`.

## 2. 2026 Tiered Memory Stack
Every cognitive cycle must utilize the standard codecs:
1. **Tier 1 (Ephemeral)**: **Flash-Optimized LZ4** for the message bus.
2. **Tier 2 (Active Context)**: **TurboQuant (QJL)** with Q8 + Binary Quantization.
3. **Tier 3 (Deep Archive)**: **LLM-Zip** (Lossless Neural Archiving) in LanceDB.

## 3. Hardware Constraints (i5-8265U)
- **TDP**: 15W.
- **Thread Limit**: Max 4 threads for SGI operations (configured in `main.py`).
- **Thermal Limit**: 78°C (monitored by `ThermalGuard`).

## 4. Verification & Safety
- **Logic**: Use `ReasonerActor` for Z3 SMT-LIB formal verification of mission-critical code.
- **Coding**: Use `CodingActor` for speculative execution in Firecracker VMs and AST-aware distillation.
- **Compliance**: **Strictly Prohibited**: GPL, LGPL, AGPL. Enforced by the `License Guardian` in `search_actor.py`.

## 5. Minimum Description Length (MDL)
- Every sleep cycle (`MemoryManager.trigger_sleep_cycle`) must review the scratchpad for patterns and synthesize knowledge into high-density Markdown entries.
- Use `AST-Aware Chunking` to preserve code context.
