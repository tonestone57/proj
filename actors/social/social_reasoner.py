import ray
from core.base import CognitiveModule

@ray.remote
class SocialReasoner(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None, episodic_memory=None):
        super().__init__(workspace, scheduler, model_registry)
        self.episodic_memory = episodic_memory
        print(f"[SocialReasoner] Initialized.")

    def receive(self, message):
        if message["type"] == "config_update":
            self.reload_config()
        elif message["type"] == "user_interaction":
            context = self.get_context()
            response = self.social_process(message["data"], context)
            try: handle = ray.get_runtime_context().current_actor
            except Exception: handle = None
            self.scheduler.submit.remote(handle, {"type": "social_response", "data": response})

    def get_context(self):
        if self.episodic_memory:
            try:
                # Handle episodic_memory as a Ray actor if applicable
                return ray.get(self.episodic_memory.recall_recent.remote(n=10))
            except Exception:
                return []
        return []

    def social_process(self, data, context):
        if self.model_registry:
            prompt = f"Context: {context}\nUser: {data}\nResponse:"
            return ray.get(self.model_registry.generate.remote(prompt))
        return f"Social response to {data}."
