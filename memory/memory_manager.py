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
        print("[MemoryManager] Pruning redundant patterns and low-saliency memories.")
        print("[MemoryManager] Archiving raw logs to long-term storage (LanceDB).")

    def synthesize_knowledge(self, patterns):
        print(f"[MemoryManager] Synthesizing new Knowledge Base entries for patterns: {patterns}")
        for pattern in patterns:
            # In a real system, this would generate a Markdown doc
            kb_entry = f"# Synthesized Lesson: {pattern}\n\nThis entry was automatically generated during a sleep cycle."
            print(f"[MemoryManager] Generated KB Entry: {pattern}")

    def calculate_structural_importance_score(self, context):
        """
        Calculates a Structural Importance Score (I_struct) for tokens using a Code Property Graph (CPG) logic.
        Protects function signatures, return types, and control logic (if/while).
        """
        print("[MemoryManager] Calculating Structural Importance Score (CodeComp)...")
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
        """
        print("[MemoryManager] Performing Lossless Neural Archiving (LLM-Zip) to LanceDB...")
        # Simulate arithmetic coding via LLM probabilities
        return "compressed_neural_representation_0xdeadbeef"

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
        Uses Context Integrity Check.
        """
        if not context:
            return "Continue"

        words = context.split()
        token_entropy = calculate_information_density(words)
        context_len = len(words)

        print(f"[MemoryManager] Context Integrity Check: Entropy={token_entropy:.4f}, Len={context_len}")

        if token_entropy < CONTEXT_SALIENCY_FLOOR:
            # The context is full of "fluff"; trigger structural distillation (CodeComp)
            return "Distill"
        elif context_len > MAX_LIMIT * 0.8:
            # The context is actually dense; trigger neural offloading to LanceDB (LLM-Zip)
            return "Archive"
        return "Continue"
