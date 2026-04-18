class EthicalEvaluator:
    def evaluate(self, action, context):
        if action.get("harm", False):
            return {"ethical": False, "reason": "harmful"}
        if context.get("violation", False):
            return {"ethical": False, "reason": "context_violation"}
        return {"ethical": True}
