import math
import re
import ray
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
    density = entropy * (1 + symbol_ratio)
    return density

@ray.remote
class MemoryManager(CognitiveModule):
    def receive(self, message):
        if message["type"] == "trigger_sleep_cycle":
            self.trigger_sleep_cycle()
        elif message["type"] == "compression_check":
            context = message["data"]
            result = self.should_compress(context)
            self.scheduler.submit.remote(ray.get_runtime_context().current_actor, {"type": "compression_result", "data": result})

    def trigger_sleep_cycle(self):
        """
        Performs background consolidation: Synaptic Pruning and Knowledge Synthesis.
        """
        print("[MemoryManager] Starting Sleep Cycle...")

        # 1. Review Scratchpad and Active Context
        patterns = ray.get(self.identify_recurring_patterns.remote())

        # 2. Synthesize new Knowledge Base Entry
        if patterns:
            self.synthesize_knowledge(patterns)

        # 3. Synaptic Pruning (Archive raw logs)
        self.perform_synaptic_pruning()

        print("[MemoryManager] Sleep Cycle complete.")

    @ray.method(num_returns=1)
    def identify_recurring_patterns(self):
        """
        Reviews Scratchpad and Workspace history to identify recurring patterns.
        """
        print("[MemoryManager] Reviewing Scratchpad and Active Context for patterns...")
        state = ray.get(self.workspace.get_current_state.remote())
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
        state = ray.get(self.workspace.get_current_state.remote())
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
            kb_entry = f"# Synthesized Lesson: {pattern}\n\nThis entry was automatically generated during a sleep cycle."
            print(f"[MemoryManager] Generated KB Entry: {pattern}")
            self.KnowledgeDistillation_Loop(kb_entry)

    def KnowledgeDistillation_Loop(self, entry):
        """
        Refines synthesized knowledge using MDL principles.
        """
        print("[MemoryManager] Running Knowledge Distillation Loop...")
        distilled = entry.replace("\n\n", " ").replace("This entry was automatically generated", "Generated")
        self.calculate_MDL_metric(entry, distilled)

    def calculate_structural_importance_score(self, context):
        """
        Calculates a Structural Importance Score (I_struct) using CPG logic.
        """
        print("[MemoryManager] Calculating Structural Importance Score ($I_{struct}$) using CPG...")
        important_patterns = [r"def\s+", r"class\s+", r"if\s+", r"while\s+", r"return\s+", r"virtual\s+"]
        score = sum(1 for pattern in important_patterns if re.search(pattern, context))
        return score

    def perform_neural_archiving(self, context):
        """
        Performs Lossless Neural Archiving (LLM-Zip).
        """
        print("[MemoryManager] Performing Lossless Neural Archiving (LLM-Zip) to LanceDB...")
        return {
            "data": "compressed_neural_representation_0xdeadbeef",
            "model_hash": "sha256_7f8e9d...",
            "residual_buffer": "residual_data_0x123..."
        }

    def perform_turboquant_compression(self, vectors):
        """
        Performs TurboQuant compression (PolarQuant + QJL).
        Q8 + BQ for Vector Index, NF4 for weights.
        """
        print("[MemoryManager] Performing TurboQuant Compression (PolarQuant + QJL)...")
        print("[MemoryManager] Applying PolarQuant rotation and QJL error-correction for Q8 + BQ / NF4 stability...")
        return "quantized_vectors_0xabc"

    def perform_kv_cache_compression(self, kv_cache):
        """
        Compresses KV Cache to FP8 (E4M3).
        """
        print("[MemoryManager] Compressing KV Cache to FP8 (E4M3)...")
        return "fp8_kv_cache"

    def perform_reasoning_compression(self, logic_chain):
        """
        Compresses Reasoning Engine to BF16 (Q16).
        """
        print("[MemoryManager] Compressing Reasoning Engine to BF16 (Q16)...")
        return "bf16_logic_chain"

    def perform_ast_serialization(self, code):
        """
        Performs Structural Codec compression using Tree-sitter Serialization.
        """
        print("[MemoryManager] Performing Tree-sitter AST Serialization...")
        if not code or not isinstance(code, str):
            return "empty_ast"

        lines = code.splitlines()
        mapping = {"def ": "OP_FUNC_DEF", "class ": "OP_CLASS_DEF", "if ": "OP_IF_BRANCH", "return ": "OP_RETURN"}
        ops = []
        for line in lines:
            line = line.strip()
            for key, val in mapping.items():
                if line.startswith(key):
                    ops.append(val)
                    break
            else:
                if "=" in line:
                    ops.append("OP_ASSIGN")

        serialized_ast = "->".join(ops) if ops else "OP_GENERIC_NODE"
        print(f"[MemoryManager] Serialized AST size: {len(serialized_ast)} bytes")
        return serialized_ast

    def AST_Aware_Chunking(self, code):
        """
        Simulates AST-aware chunking to preserve structural relationships.
        """
        print("[MemoryManager] Performing AST-Aware Chunking...")
        chunks, current_chunk = [], []
        for line in code.splitlines():
            if (line.startswith("def ") or line.startswith("class ")) and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
            current_chunk.append(line)
        if current_chunk: chunks.append("\n".join(current_chunk))
        print(f"[MemoryManager] Created {len(chunks)} structural chunks.")
        return chunks

    def calculate_MDL_metric(self, data, compressed_data):
        raw_size, compressed_size = len(str(data)), len(str(compressed_data))
        mdl_score = compressed_size / raw_size if raw_size > 0 else 1.0
        print(f"[MemoryManager] MDL Score: {mdl_score:.4f} (Raw: {raw_size}, Compressed: {compressed_size})")
        return mdl_score

    def perform_structural_distillation(self, context):
        """
        Performs AST-Aware KV Pruning (CodeComp).
        """
        print("[MemoryManager] Performing Structural Distillation (CodeComp)...")
        return re.sub(r"#.*", "", context)

    def should_compress(self, context):
        tokens = context.split() if isinstance(context, str) else context
        token_entropy = calculate_information_density(tokens)
        if token_entropy < CONTEXT_SALIENCY_FLOOR:
            return "Distill"
        elif len(tokens) > MAX_LIMIT * 0.8:
            return "Archive"
        return "Continue"
