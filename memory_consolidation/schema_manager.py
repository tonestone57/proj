from core.base import CognitiveModule

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
        category = partial_memory.get("category")
        if category in self.schemas:
            schema = self.schemas[category]
            enriched = partial_memory.copy()
            enriched["features"] = {
                **schema["features"],
                **partial_memory.get("features", {})
            }
            return enriched
        return partial_memory

