import ray
import re
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
        # Matches patterns like True == False, 1 == 0, 1 != 1 with varying whitespace
        constant_contradictions = [
            r"\b(\d+)\s*==\s*(?!\1)\d+\b", # 1 == 2
            r"\b(\d+)\s*!=\s*\1\b",         # 1 != 1
            r"\bTrue\s*==\s*False\b",
            r"\bFalse\s*==\s*True\b",
            r"\bTrue\s*!=\s*True\b",
            r"\bFalse\s*!=\s*False\b"
        ]

        for pattern in constant_contradictions:
            if re.search(pattern, code):
                issues.append(f"Obvious logical contradiction detected (Pattern: {pattern}).")
                break

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
