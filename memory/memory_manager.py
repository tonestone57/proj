import math
import re
import psutil
import time
import ray
import lancedb
import pandas as pd
from sentence_transformers import SentenceTransformer
from core.base import CognitiveModule
from core.config import CONTEXT_SALIENCY_FLOOR, MAX_LIMIT, PRUNING_THRESHOLD_PCT, ACTIVE_CONTEXT_LIMIT, LOW_MEMORY_WARNING_MB

def calculate_information_density(words):
    if not words: return 0.0
    counts, total_chars, symbols = {}, 0, set("!@#$%^&*()_+-=[]{}|;':\",./<>?")
    symbol_count = 0
    for word in words:
        counts[word] = counts.get(word, 0) + 1
        total_chars += len(word)
        for char in word:
            if char in symbols: symbol_count += 1
    total_words = len(words)
    entropy = sum(-(count/total_words) * math.log2(count/total_words) for count in counts.values())
    symbol_ratio = symbol_count / total_chars if total_chars > 0 else 0
    return entropy * (1 + symbol_ratio)

@ray.remote
class MemoryManager(CognitiveModule):
    def __init__(self, workspace, scheduler):
        super().__init__(workspace, scheduler)
        self.context_buffer = [] # Active Context
        self.active_context_limit = ACTIVE_CONTEXT_LIMIT
        # Use a lightweight model optimized for CPU AVX2 on 8265U
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.db = lancedb.connect("./data/sgi_archived_memory")
        self.table = None

    def receive(self, message):
        if message["type"] == "trigger_sleep_cycle":
            self.trigger_sleep_cycle()
        elif message["type"] == "compression_check":
            context = message["data"]
            result = self.should_compress(context)
            # In Ray, scheduler is a remote actor
            self.scheduler.submit.remote(ray.get_runtime_context().get_actor_handle(), {"type": "compression_result", "data": result})
        elif message["type"] == "add_to_context":
            self.context_buffer.append(message["data"])
            self.manage_context()

    def memory_swap_guard(self):
        mem = psutil.virtual_memory()
        if mem.available < 1024 * 1024 * LOW_MEMORY_WARNING_MB:
            print("🚨 Memory Swap Guard: RAM dangerously low!")
            return False
        return True

    def archive_nugget(self, summary_text):
        """Vector Searchable Memory (Section 4)."""
        print(f"[MemoryManager] Archiving nugget: {summary_text[:50]}...")
        vector = self.embed_model.encode(summary_text)
        data = [{"vector": vector, "text": summary_text, "timestamp": time.time()}]
        if self.table is None:
            if "memory" in self.db.table_names():
                self.table = self.db.open_table("memory")
                self.table.add(data)
            else:
                self.table = self.db.create_table("memory", data=data)
        else:
            self.table.add(data)

    def retrieve_relevant(self, query):
        if self.table is None: return []
        query_vec = self.embed_model.encode(query)
        return self.table.search(query_vec).limit(2).to_list()

    def manage_context(self):
        current_usage = sum(len(m.split()) * 1.3 for m in self.context_buffer)
        if current_usage > (self.active_context_limit * PRUNING_THRESHOLD_PCT):
            print("⚠️ Context Pruning Triggered (80% Limit reached)")
            to_archive = " ".join(self.context_buffer[:5])
            self.archive_nugget(to_archive)
            summary = "Synthesized Memory Nugget from pruned context." # In real usage, use 4-bit summarizer
            self.context_buffer = [f"System Summary: {summary}"] + self.context_buffer[5:]
            return "Context Pruned & Archived."
        return "Context Stable."

    def trigger_sleep_cycle(self):
        print("[MemoryManager] Starting Sleep Cycle...")
        if self.memory_swap_guard():
            patterns = self.identify_recurring_patterns()
            if patterns: self.synthesize_knowledge(patterns)
        print("[MemoryManager] Sleep Cycle complete.")

    def identify_recurring_patterns(self):
        # We need to await the remote call to workspace
        state = ray.get(self.workspace.get_current_state.remote())
        history = state.get("history", [])
        return ["Frequent interaction with Haiku OS BMessage syntax"] if sum(1 for msg in history if "Haiku OS" in str(msg)) > 3 else []

    def perform_synaptic_pruning(self):
        print("[MemoryManager] Pruning redundant patterns and low-saliency memories.")

    def synthesize_knowledge(self, patterns):
        for pattern in patterns:
            self.archive_nugget(f"Synthesized Lesson: {pattern}")

    def should_compress(self, context):
        token_entropy = calculate_information_density(context.split() if isinstance(context, str) else context)
        if token_entropy < CONTEXT_SALIENCY_FLOOR: return "Distill"
        elif len(context.split() if isinstance(context, str) else context) > MAX_LIMIT * 0.8: return "Archive"
        return "Continue"
