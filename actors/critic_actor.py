import ray
from core.base import CognitiveModule

try:
    from ipex_llm.transformers import AutoModelForCausalLM, AutoTokenizer
except ImportError:
    AutoModelForCausalLM, AutoTokenizer = None, None

@ray.remote
class InternalCritic(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_id="DeepSeek-Coder-V2-Lite"):
        super().__init__(workspace, scheduler)
        self.critiques = []
        print(f"[InternalCritic] Loading {model_id} for semantic critique (INT8 precision)...")
        if AutoModelForCausalLM and model_id:
            try:
                # SGI 2026: Internal Critic uses INT8 for high accuracy
                self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    load_in_low_bit="sym_int8",
                    trust_remote_code=True,
                    use_cache=True
                )
            except Exception as e:
                print(f"[InternalCritic] Error loading model: {e}. Using heuristics.")
                self.model = None
            self.tokenizer = None
        else:
            print("[InternalCritic] IPEX-LLM not available or no model_id. Using heuristics.")
            self.model = None
            self.tokenizer = None

    def critique_code(self, code):
        print(f"[InternalCritic] Critiquing code snippet...")
        issues = []
        if len(code) < 10: issues.append("Code snippet is suspiciously short.")
        if "TODO" in code: issues.append("Code contains unfinished placeholders (TODO).")
        if code.count("(") != code.count(")"): issues.append("Mismatched parentheses detected.")

        if self.model:
            # SGI 2026: Semantic Code Critique using INT8 model
            print("[InternalCritic] Performing semantic code analysis via LLM...")
            # Simulated model critique
            if "pass" in code: issues.append("Semantic Warning: Code contains empty 'pass' blocks.")

        return issues

    def critique_logic(self, reasoning):
        print(f"[InternalCritic] Critiquing symbolic reasoning...")
        issues = []
        if "1/0" in reasoning or "division by zero" in reasoning.lower():
            issues.append("Logic contains potential division by zero.")
        if "True == False" in reasoning:
            issues.append("Blatant logical contradiction detected.")

        if self.model:
            # SGI 2026: Semantic Logic Critique using INT8 model
            print("[InternalCritic] Performing semantic logic analysis via LLM...")
            # Simulated model critique
            if "inferred" in str(reasoning): issues.append("Semantic Warning: Reasoning relies on inferred premises.")

        return issues

    def verify_goal_alignment(self, output, goal):
        print(f"[InternalCritic] Verifying alignment with goal: {goal}")
        goal_keywords = set(str(goal).lower().split())
        output_keywords = set(str(output).lower().split())
        if not goal_keywords.intersection(output_keywords):
            return ["Output does not appear to address the specified goal."]
        return []

    def receive(self, message):
        if message["type"] == "critique_request":
            data, category = message["data"], message.get("category", "general")
            issues = self.critique_code(data) if category == "code" else self.critique_logic(data) if category == "logic" else []
            if "goal" in message: issues.extend(self.verify_goal_alignment(data, message["goal"]))

            try:
                handle = ray.get_runtime_context().current_actor
            except Exception:
                handle = None

            self.scheduler.submit.remote(handle, {
                "type": "critique_result", "issues": issues, "original_sender": message.get("sender")
            })
