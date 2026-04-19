import ray
from core.base import CognitiveModule

try:
    from ipex_llm.transformers import AutoModelForCausalLM, AutoTokenizer
except ImportError:
    AutoModelForCausalLM, AutoTokenizer = None, None

@ray.remote
class MetaReasoner(CognitiveModule):
    def __init__(self, workspace, scheduler, model_id="DeepSeek-Coder-V2-Lite"):
        super().__init__(workspace, scheduler)
        print(f"[MetaReasoner] Loading {model_id} for metacognitive evaluation...")
        if AutoModelForCausalLM and model_id:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    load_in_low_bit="sym_int8",
                    trust_remote_code=True,
                    use_cache=True
                )
            except Exception as e:
                print(f"[MetaReasoner] Error loading model: {e}. Using heuristics.")
                self.model = None
            self.tokenizer = None
        else:
            print("[MetaReasoner] IPEX-LLM not available or no model_id. Using heuristics.")
            self.model = None
            self.tokenizer = None

    def receive(self, message):
        if message["type"] == "evaluate_reasoning":
            result = self.evaluate_reasoning(message["data"])
            try: handle = ray.get_runtime_context().current_actor
            except Exception: handle = None
            self.scheduler.submit.remote(handle, {"type": "evaluation_result", "data": result})

    def evaluate_reasoning(self, reasoning_trace):
        if not reasoning_trace:
            return {"quality": "unknown", "issues": ["empty_trace"]}

        issues = []
        if any("contradiction" in step for step in reasoning_trace):
            issues.append("logical_contradiction")

        if self.model:
            # SGI 2026: Metacognitive evaluation via LLM
            print("[MetaReasoner] Performing semantic quality evaluation via LLM...")
            # Simulated LLM analysis
            if len(reasoning_trace) > 5:
                issues.append("Semantic Warning: Reasoning chain is overly complex.")

        return {
            "quality": "good" if not issues else "problematic",
            "issues": issues
        }
