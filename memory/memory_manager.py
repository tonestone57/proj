import math
from core.base import CognitiveModule

CONTEXT_SALIENCY_FLOOR = 0.5
MAX_LIMIT = 8192

def calculate_information_density(words):
    """
    Computes token-level entropy of the provided list of words.
    """
    if not words:
        return 0.0

    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1

    total = len(words)
    entropy = 0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy

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
