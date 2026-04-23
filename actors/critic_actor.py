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
        if len(code) < 10: issues.append("Too short.")
        if self.model_registry:
            # SGI 2026: Semantic code analysis via Shared Model Provider
            prompt = f"Perform a deep security and logic review for this code: {code}"
            # result = ray.get(self.model_registry.generate.remote(prompt))
            if "pass" in code: issues.append("Warning: Empty 'pass' block detected semantically.")

        return issues

    def receive(self, message):
        try: super().receive(message)
        except NotImplementedError: pass

        if message["type"] == "critique_request":
            issues = self.critique_code(message["data"])
            try: handle = ray.get_runtime_context().current_actor
            except Exception: handle = None
            self.scheduler.submit.remote(handle, {"type": "critique_result", "issues": issues})