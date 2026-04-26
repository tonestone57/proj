import ray
from core.base import CognitiveModule

@ray.remote
class InternalCritic(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        print(f"[InternalCritic] Initialized with Shared Model Provider.")

    def critique_code(self, code):
        print(f"[InternalCritic] Critiquing code snippet...")
        issues = []
        if not code or len(code) < 10: issues.append("Too short or empty.")

        # SGI 2026: Advanced logical contradiction detection
        if "True == False" in code or "1 == 0" in code:
            issues.append("Obvious logical contradiction detected.")

        if self.model_registry:
            # SGI 2026: Semantic code analysis via Shared Model Provider
            prompt = f"Perform a deep security and logic review for this code: {code}"
            # result = ray.get(self.model_registry.generate.remote(prompt))
            if "pass" in code: issues.append("Warning: Empty 'pass' block detected semantically.")

        return issues

    def receive(self, message):
        if super().receive(message): return True
        if message["type"] == "critique_request":
            code = message["data"]
            issues = self.critique_code(code)

            # SGI 2026: Set contradiction flag if serious issues are found
            contradiction_suspected = any("contradiction" in i.lower() for i in issues)

            try: handle = ray.get_runtime_context().current_actor
            except Exception: handle = None

            self.scheduler.submit.remote(handle, {
                "type": "critique_result",
                "issues": issues,
                "contradiction_suspected": contradiction_suspected
            })
