import ray
from core.base import CognitiveModule

@ray.remote
class TheoryOfMind(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.agent_models = {}
        print(f"[TheoryOfMind] Initialized with Shared Model Provider.")

    def receive(self, message):
        if message["type"] == "social_event":
            self.update_agent_model(message["agent"], message["data"])

        if message["type"] == "infer_intention":
            intention = self.infer_intention(message["agent"])
            try: handle = ray.get_runtime_context().current_actor
            except Exception: handle = None
            self.scheduler.submit.remote(handle, {
                "type": "intention_inferred",
                "agent": message["agent"],
                "data": intention
            })

    def update_agent_model(self, agent, data):
        if agent not in self.agent_models:
            self.agent_models[agent] = {"beliefs": {}, "goals": {}, "emotions": {}, "history": []}
        self.agent_models[agent]["history"].append(data)

    def infer_intention(self, agent):
        print(f"[TheoryOfMind] Inferring intention for agent: {agent}")
        if self.model_registry:
            # SGI 2026: Complex intention inference via Shared Model Provider
            prompt = f"Analyze agent history for {agent} and infer their current goal and mental state."
            return ray.get(self.model_registry.generate.remote(prompt))

        return {"intention": "uncertain", "confidence": 0.5}
