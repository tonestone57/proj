import ray
from core.base import CognitiveModule

@ray.remote # SGI 2026: Standardized Ray Actor
class MetaReasoner(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        print(f"[MetaReasoner] Initialized with Shared Model Provider.")

    def receive(self, message):
        if super().receive(message): return
        if message["type"] == "evaluate_reasoning":
            result = self.evaluate_reasoning(message["data"])
            self.send_result("evaluation_result", result)

    def evaluate_reasoning(self, trace):
        print(f"[MetaReasoner] Evaluating reasoning trace via Shared Model Provider...")
        if self.model_registry:
            # SGI 2026: Semantic quality evaluation via LLM inference
            prompt = f"Critically evaluate this reasoning chain for logical consistency and depth. Return a JSON with 'score' (0-1) and 'feedback'. Trace: {trace}"
            try:
                # Handle both Ray remote objects and local objects for testing
                if hasattr(self.model_registry.generate, "remote"):
                    response = ray.get(self.model_registry.generate.remote(prompt))
                else:
                    response = self.model_registry.generate(prompt)
                return {"status": "success", "evaluation": response}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        return {"status": "mock", "score": 0.8, "feedback": "Logic appears consistent."}
