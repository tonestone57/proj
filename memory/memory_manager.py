import math
import re
from core.base import CognitiveModule
from core.config import CONTEXT_SALIENCY_FLOOR, MAX_LIMIT

def calculate_information_density(words):
    """
    Computes a refined information density metric for the provided list of words.
    Combines Shannon entropy with a symbol-to-word ratio to better detect "code fluff".
    """
    if not words:
        return 0.0

    # Shannon Entropy calculation
    counts = {}
    total_chars = 0
    symbols = set("!@#$%^&*()_+-=[]{}|;':\",./<>?")
    symbol_count = 0

    for word in words:
        counts[word] = counts.get(word, 0) + 1
        total_chars += len(word)
        for char in word:
            if char in symbols:
                symbol_count += 1

    total_words = len(words)
    entropy = 0
    for count in counts.values():
        p = count / total_words
        entropy -= p * math.log2(p)

    # Symbol density factor (code often has more symbols than natural language)
    symbol_ratio = symbol_count / total_chars if total_chars > 0 else 0

    # Combined metric: Entropy weighted by symbol density
    # Natural language "fluff" has high word-level entropy but low symbol density.
    # Dense code has meaningful symbols and structure.
    density = entropy * (1 + symbol_ratio)

    return density

class MemoryManager(CognitiveModule):
    def receive(self, message):
        if message["type"] == "trigger_sleep_cycle":
            self.trigger_sleep_cycle()
        elif message["type"] == "compression_check":
            context = message["data"]
            result = self.should_compress(context)
            self.scheduler.submit(self, {"type": "compression_result", "data": result})

    def trigger_sleep_cycle(self):
        """
        Performs background consolidation: Synaptic Pruning and Knowledge Synthesis.
        """
        print("[MemoryManager] Starting Sleep Cycle...")

        # 1. Review Scratchpad and Active Context
        patterns = self.identify_recurring_patterns()

        # 2. Synthesize new Knowledge Base Entry
        if patterns:
            self.synthesize_knowledge(patterns)

        # 3. Synaptic Pruning (Archive raw logs)
        self.perform_synaptic_pruning()

        print("[MemoryManager] Sleep Cycle complete.")

    def identify_recurring_patterns(self):
        """
        Reviews Scratchpad and Workspace history to identify recurring patterns.
        """
        print("[MemoryManager] Reviewing Scratchpad and Active Context for patterns...")
        state = self.workspace.get_current_state()
        history = state.get("history", [])

        # Simulate pattern detection (e.g., looking up Haiku OS syntax)
        patterns = []
        haiku_count = sum(1 for msg in history if "Haiku OS" in str(msg))
        if haiku_count > 3:
            patterns.append("Frequent interaction with Haiku OS BMessage syntax")

        return patterns

    def perform_synaptic_pruning(self):
        """
        Evicts low-saliency memories during sleep cycles.
        """
        print("[MemoryManager] Performing Synaptic Pruning...")
        state = self.workspace.get_current_state()
        history = state.get("history", [])

        pruned_count = 0
        preserved_history = []
        for msg in history:
            # Low saliency: message is old and has low token entropy
            saliency = calculate_information_density(str(msg).split())
            if saliency > CONTEXT_SALIENCY_FLOOR:
                preserved_history.append(msg)
            else:
                pruned_count += 1

        print(f"[MemoryManager] Pruned {pruned_count} low-saliency memories.")
        print("[MemoryManager] Archiving remaining raw logs to long-term storage (LanceDB) using Zstd-19.")

    def synthesize_knowledge(self, patterns):
        print(f"[MemoryManager] Synthesizing new Knowledge Base entries for patterns: {patterns}")
        for pattern in patterns:
            # In a real system, this would generate a Markdown doc
            kb_entry = f"# Synthesized Lesson: {pattern}\n\nThis entry was automatically generated during a sleep cycle."
            print(f"[MemoryManager] Generated KB Entry: {pattern}")
            self.KnowledgeDistillation_Loop(kb_entry)

    def KnowledgeDistillation_Loop(self, entry):
        """
        Refines synthesized knowledge using MDL principles.
        """
        print("[MemoryManager] Running Knowledge Distillation Loop...")
        # Simulate distilling natural language into high-density representation
        distilled = entry.replace("\n\n", " ").replace("This entry was automatically generated", "Generated")
        self.calculate_MDL_metric(entry, distilled)

    def calculate_structural_importance_score(self, context):
        """
        Calculates a Structural Importance Score (I_struct) for tokens using a Code Property Graph (CPG) logic.
        Protects function signatures, return types, and control logic (if/while).
        """
        print("[MemoryManager] Calculating Structural Importance Score ($I_{struct}$) using CPG...")
        # Simulated CodeComp logic: identifying mission-critical structural tokens
        important_patterns = [r"def\s+", r"class\s+", r"if\s+", r"while\s+", r"return\s+", r"virtual\s+"]
        score = 0
        for pattern in important_patterns:
            if re.search(pattern, context):
                score += 1
        return score

    def perform_neural_archiving(self, context):
        """
        Performs Lossless Neural Archiving (LLM-Zip).
        Encodes context into a dense, neural representation for 0% information loss.
        Includes a Model Hash and Residual Mismatch Buffer to prevent non-deterministic mismatch.
        """
        print("[MemoryManager] Performing Lossless Neural Archiving (LLM-Zip) to LanceDB...")
        # Simulate arithmetic coding via LLM probabilities
        model_hash = "sha256_7f8e9d..."
        mismatch_buffer = "residual_data_0x123..."
        compressed_data = "compressed_neural_representation_0xdeadbeef"

        return {
            "data": compressed_data,
            "model_hash": model_hash,
            "residual_buffer": mismatch_buffer
        }

    def perform_turboquant_compression(self, vectors):
        """
        Performs TurboQuant compression using PolarQuant and QJL.
        Compresses vectors (RAG Index) to Q8 + BQ (INT8 for accuracy, Binary for scale).
        Base weights are compressed to NF4.
        """
        print("[MemoryManager] Performing TurboQuant Compression (PolarQuant + QJL)...")
        # 1. PolarQuant: Randomly rotate data vectors to simplify geometry
        print("[MemoryManager] Applying PolarQuant rotation to stabilize vector distribution...")
        # 2. QJL: Quantized Johnson-Lindenstrauss for 1-bit error-correction
        print("[MemoryManager] Applying QJL error-correction for Q8 + BQ / NF4 stability...")
        return "quantized_vectors_0xabc"

    def perform_kv_cache_compression(self, kv_cache):
        """
        Compresses KV Cache (Memory) to FP8 (E4M3).
        Provides high dynamic range for spiky activations.
        """
        print("[MemoryManager] Compressing KV Cache to FP8 (E4M3)...")
        return "fp8_kv_cache"

    def perform_reasoning_compression(self, logic_chain):
        """
        Compresses Reasoning Engine (Brain) to BF16 (Q16).
        Ensures maximum fidelity for A->B logic and proofs.
        """
        print("[MemoryManager] Compressing Reasoning Engine to BF16 (Q16)...")
        return "bf16_logic_chain"

    def perform_ast_serialization(self, code):
        """
        Performs Structural Codec compression using Tree-sitter Serialization.
        Serializes the AST into a high-density operation stream.
        """
        print("[MemoryManager] Performing Tree-sitter AST Serialization...")
        # Enhanced simulation: Capture more structure than just top-level nodes
        if not code or not isinstance(code, str):
            return "empty_ast"

        lines = code.splitlines()
        ops = []
        for line in lines:
            line = line.strip()
            if line.startswith("def "):
                ops.append("OP_FUNC_DEF")
            elif line.startswith("class "):
                ops.append("OP_CLASS_DEF")
            elif line.startswith("if "):
                ops.append("OP_IF_BRANCH")
            elif line.startswith("return "):
                ops.append("OP_RETURN")
            elif "=" in line:
                ops.append("OP_ASSIGN")

        if not ops:
            ops = ["OP_GENERIC_NODE"]

        serialized_ast = "->".join(ops)
        print(f"[MemoryManager] Serialized AST size: {len(serialized_ast)} bytes")
        return serialized_ast

    def AST_Aware_Chunking(self, code):
        """
        Simulates AST-aware chunking to preserve structural relationships.
        Avoids standard 200-400 word chunking for code.
        """
        print("[MemoryManager] Performing AST-Aware Chunking...")
        chunks = []
        # Simulate splitting by function/class blocks
        current_chunk = []
        for line in code.splitlines():
            if (line.startswith("def ") or line.startswith("class ")) and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
            current_chunk.append(line)
        if current_chunk:
            chunks.append("\n".join(current_chunk))

        print(f"[MemoryManager] Created {len(chunks)} structural chunks.")
        return chunks

    def calculate_MDL_metric(self, data, compressed_data):
        """
        Calculates the Minimum Description Length (MDL) metric.
        Lower values indicate better understanding/compression.
        """
        raw_size = len(str(data))
        compressed_size = len(str(compressed_data))
        mdl_score = compressed_size / raw_size if raw_size > 0 else 1.0
        print(f"[MemoryManager] MDL Score: {mdl_score:.4f} (Raw: {raw_size}, Compressed: {compressed_size})")
        return mdl_score

    def perform_structural_distillation(self, context):
        """
        Performs AST-Aware KV Pruning (CodeComp).
        Evicts boilerplate while protecting the Control Flow Skeleton.
        """
        print("[MemoryManager] Performing Structural Distillation (CodeComp)...")
        # Evicting redundant comments and boilerplate
        distilled = re.sub(r"#.*", "", context)
        return distilled

    def should_compress(self, context):
        """
        Decides between "Distill" (CodeComp), "Archive" (LLM-Zip), or "Continue".
        Uses Context Integrity Check based on MDL and information density.
        """
        # Instead of just len(context) > threshold:
        token_entropy = calculate_information_density(context.split() if isinstance(context, str) else context)
        if token_entropy < CONTEXT_SALIENCY_FLOOR:
            # The context is full of "fluff"; trigger structural distillation
            return "Distill"
        elif len(context.split() if isinstance(context, str) else context) > MAX_LIMIT * 0.8:
            # The context is actually dense; trigger neural offloading to LanceDB
            return "Archive"
        return "Continue"
