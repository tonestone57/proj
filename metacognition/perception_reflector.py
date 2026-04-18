class PerceptionReflector:
    def evaluate_perception(self, sensory_input):
        if sensory_input is None:
            return {"status": "error", "issue": "missing_input"}
        return {"status": "ok"}
