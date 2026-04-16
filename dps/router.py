class TaskRouter:
    def __init__(self, module_registry):
        self.module_registry = module_registry

    def route(self, message):
        msg_type = message.get("type")

        # Example routing logic
        if msg_type in ["image_input", "vision_output"]:
            return self.module_registry.get("vision")

        if msg_type in ["query", "symbolic_result"]:
            return self.module_registry.get("symbolic_reasoner")

        if msg_type in ["goal", "plan"]:
            return self.module_registry.get("planner")

        if msg_type.startswith("internal_"):
            return self.module_registry.get("self_model")

        if msg_type in ["code_execution", "code_result"]:
            return self.module_registry.get("coding")

        if msg_type in ["user_interaction", "social_response"]:
            return self.module_registry.get("social")

        return None
