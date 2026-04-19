import ray
from core.base import CognitiveModule

@ray.remote
class InternalCritic(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_id=None):
        super().__init__(workspace, scheduler)
        self.critiques = []

    def critique_code(self, code):
        print(f"[InternalCritic] Critiquing code snippet...")
        issues = []
        if len(code) < 10: issues.append("Code snippet is suspiciously short.")
        if "TODO" in code: issues.append("Code contains unfinished placeholders (TODO).")
        if code.count("(") != code.count(")"): issues.append("Mismatched parentheses detected.")
        return issues

    def critique_logic(self, reasoning):
        print(f"[InternalCritic] Critiquing symbolic reasoning...")
        issues = []
        if "1/0" in reasoning or "division by zero" in reasoning.lower():
            issues.append("Logic contains potential division by zero.")
        if "True == False" in reasoning:
            issues.append("Blatant logical contradiction detected.")
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
            self.scheduler.submit.remote(ray.get_runtime_context().current_actor, {
                "type": "critique_result", "issues": issues, "original_sender": message.get("sender")
            })
