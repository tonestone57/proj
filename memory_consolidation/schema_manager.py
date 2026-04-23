import ray
from core.base import CognitiveModule

@ray.remote
class SchemaManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.schemas = {}

    def update_schema(self, episode):
        category = episode.get("category")
        if category not in self.schemas:
            self.schemas[category] = {"count": 0, "features": {}}

        schema = self.schemas[category]
        schema["count"] += 1

        for k, v in episode.get("features", {}).items():
            schema["features"][k] = schema["features"].get(k, 0) + v

    def apply_schema(self, partial_memory):
        # SGI 2026: Apply prototypical schema to reconstruct partial memories
        category = partial_memory.get("category")
        if category not in self.schemas:
            return partial_memory

        schema = self.schemas[category]
        count = schema["count"]

        reconstructed = partial_memory.copy()
        for k, total_val in schema["features"].items():
            if k not in reconstructed:
                # Fill in missing data with schema average
                reconstructed[k] = total_val / count

        return reconstructed

    def get_known_categories(self):
        return list(self.schemas.keys())

    def receive(self, message):
        try: super().receive(message)
        except NotImplementedError: pass
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "update_schema":
            self.update_schema(message["data"])
        elif message["type"] == "apply_schema":
            result = self.apply_schema(message["data"])
            self.send_result("schema_result", result)