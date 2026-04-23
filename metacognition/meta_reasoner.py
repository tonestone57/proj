from core.base import CognitiveModule
import ray

class MetaReasoner(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        print(f"[MetaReasoner] Initialized with Shared Model Provider.")

    def receive(self, message):
        if message["type"] == "evaluate_reasoning":
            result = self.evaluate_reasoning(message["data"])
            try: handle = ray.get_runtime_context().current_actor
            except Exception: handle = None
            self.scheduler.submit.remote(handle, {"type": "evaluation_result", "data": result})

    def evaluate_reasoning(self, trace):
        import ray
        print(f"[MetaReasoner] Evaluating reasoning trace via Shared Model Provider...")
        if self.model_registry:
            # SGI 2026: Semantic quality evaluation via LLM inference
            prompt = f"Critically evaluate this reasoning chain for logical consistency and depth. Return a JSON with 'score' (0-1) and 'feedback'. Trace: {trace}"
            try:
                response = ray.get(self.model_registry.generate.remote(prompt))
                return {"status": "success", "evaluation": response}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        return {"status": "mock", "score": 0.8, "feedback": "Logic appears consistent."}
