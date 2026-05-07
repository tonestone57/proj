import logging
import ray
import re
from core.base import CognitiveModule

# Standard SGI 2026 Logging
logger = logging.getLogger(__name__)

@ray.remote
class InternalCritic(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        logger.error(f"Initialized with Shared Model Provider.")

    def critique_code(self, code, context=None):
        """
        SGI 2026 Reflector/Judge logic.
        Performs detailed critique and assigns a quality score.
        """
        logger.error(f"Critiquing code snippet...")
        issues = []
        score = 1.0

        if not code:
            return ["Empty code."], 0.0

        if len(code) < 10:
            issues.append("Code is too short to be functional.")
            score -= 0.3

        # SGI 2026: Advanced logical contradiction detection
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
                score -= 0.5
                break

        # SGI 2026: Best practice checks
        if "except:" in code:
            issues.append("Bare except block detected. Recommend catching specific exceptions.")
            score -= 0.1

        if "eval(" in code:
            issues.append("Security risk: Use of 'eval()' detected.")
            score -= 0.2

        if self.model_registry:
            # SGI 2026: Semantic code analysis via Shared Model Provider (Tier 3 Reflector)
            prompt = f"Act as a Senior AI Architect. Perform a deep logic, security, and MDL efficiency review for this code:\n{code}"
            if context:
                prompt += f"\nContext: {context}"

            try:
                # We simulate a deep critique
                llm_critique = ray.get(self.model_registry.generate.remote(prompt))
                if "<thought>" in llm_critique:
                    llm_critique = re.sub(r"<thought>.*?</thought>\s*", "", llm_critique, flags=re.DOTALL)

                # Heuristic scoring based on LLM response length and keywords
                if "error" in llm_critique.lower() or "bug" in llm_critique.lower():
                    score -= 0.2
                if "optimize" in llm_critique.lower():
                    issues.append(f"Optimization suggested: {llm_critique[:100]}...")
            except Exception as e:
                logger.error(f"LLM critique failed: {e}")

        # Ensure score stays in [0, 1]
        score = max(0.0, min(1.0, score))

        return issues, score

    def receive(self, message):
        if super().receive(message): return True
        if message["type"] == "critique_request":
            data = message["data"]
            code = data.get("code") if isinstance(data, dict) else data
            context = data.get("context") if isinstance(data, dict) else None

            issues, score = self.critique_code(code, context=context)

            # SGI 2026: Set contradiction flag if serious issues are found
            contradiction_suspected = score < 0.5 or any("contradiction" in i.lower() for i in issues)

            try: handle = ray.get_runtime_context().current_actor
            except Exception: handle = None

            self.scheduler.submit.remote(handle, {
                "type": "critique_result",
                "issues": issues,
                "score": score,
                "contradiction_suspected": contradiction_suspected,
                "code": code
            })