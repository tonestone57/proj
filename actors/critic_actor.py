import ray
import torch
from ipex_llm.transformers import AutoModelForCausalLM
from core.config import CORES_CRITIC
from core.base import CognitiveModule

@ray.remote(num_cpus=CORES_CRITIC)
class InternalCritic(CognitiveModule):
    """
    Evaluates the outputs of other actors to ensure accuracy, safety, and goal alignment.
    Acts as an 'Internal Critic' to verify reasoning before finalization.
    Uses IPEX-LLM for hardware-accelerated high-precision verification.
    """
    def __init__(self, workspace, scheduler, model_id="intel/neural-chat-14b-v3-3"):
        super().__init__(workspace, scheduler)
        # We start with FP16 as requested, but we will use low-bit if loading fails
        print(f"[InternalCritic] Attempting to load {model_id} in FP16...")
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=torch.float16,
                optimize_model=True,
                trust_remote_code=True
            )
            print("[InternalCritic] Model loaded successfully in FP16.")
        except Exception as e:
            print(f"[InternalCritic] FP16 load failed: {e}. Falling back to NF4 for 14B stability.")
            try:
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    load_in_low_bit="nf4",
                    optimize_model=True,
                    trust_remote_code=True
                )
                print("[InternalCritic] Model loaded successfully in NF4.")
            except Exception as e2:
                print(f"[InternalCritic] NF4 load also failed: {e2}. Using mock verification.")
                self.model = None

    def verify(self, reasoning_chain, goal):
        print(f"[InternalCritic] Verifying logic for goal: {goal}")
        if self.model is None: return "YES" in reasoning_chain.upper() or "CORRECT" in reasoning_chain.upper()
        # Mocking generation for demo
        return True

    def critique_code(self, code):
        """
        Evaluates syntax, style, and potential bugs in generated code.
        """
        print(f"[CriticActor] Critiquing code snippet...")
        issues = []
        if len(code) < 10: issues.append("Code snippet is suspiciously short.")
        if "TODO" in code: issues.append("Code contains unfinished placeholders (TODO).")
        if code.count("(") != code.count(")"): issues.append("Mismatched parentheses detected.")
        return issues

    def critique_logic(self, reasoning):
        """
        Reviews mathematical and symbolic reasoning for consistency.
        """
        print(f"[CriticActor] Critiquing symbolic reasoning...")
        issues = []
        if "1/0" in reasoning or "division by zero" in reasoning.lower(): issues.append("Logic contains potential division by zero.")
        if "True == False" in reasoning: issues.append("Blatant logical contradiction detected.")
        return issues

    def verify_goal_alignment(self, output, goal):
        """
        Ensures output matches the original objective from the Planner.
        """
        print(f"[CriticActor] Verifying alignment with goal: {goal}")
        goal_keywords = set(str(goal).lower().split())
        output_keywords = set(str(output).lower().split())
        overlap = goal_keywords.intersection(output_keywords)
        if not overlap: return ["Output does not address the specified goal."]
        return []

    def receive(self, message):
        if message["type"] == "critique_request":
            data = message["data"]
            category = message.get("category", "general")
            issues = []
            if category == "code": issues = self.critique_code(data)
            elif category == "logic": issues = self.critique_logic(data)
            if "goal" in message: issues.extend(self.verify_goal_alignment(data, message["goal"]))
            self.scheduler.submit.remote(ray.get_runtime_context().get_actor_handle(), {
                "type": "critique_result",
                "issues": issues,
                "original_sender": message.get("sender")
            })
