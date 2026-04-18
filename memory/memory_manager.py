import math
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
        self.perform_synaptic_pruning()
        self.synthesize_knowledge()
        print("[MemoryManager] Sleep Cycle complete.")

    def perform_synaptic_pruning(self):
        print("[MemoryManager] Pruning redundant patterns and low-saliency memories.")

    def synthesize_knowledge(self):
        print("[MemoryManager] Synthesizing new Knowledge Base entries from recent logs.")

    def should_compress(self, context):
        """
        Decides between "Distill", "Archive", or "Continue".
        """
        if not context:
            return "Continue"

        words = context.split()
        density = calculate_information_density(words)
        context_len = len(words)

        if density < CONTEXT_SALIENCY_FLOOR:
            # The context is full of "fluff"; trigger structural distillation
            return "Distill"
        elif context_len > MAX_LIMIT * 0.8:
            # The context is actually dense; trigger neural offloading to LanceDB
            return "Archive"
        return "Continue"
