class SafetyHooks:
    def validate(self, action):
        if action.get("dangerous", False):
            return {"safe": False, "reason": "safety_violation"}
        return {"safe": True}
