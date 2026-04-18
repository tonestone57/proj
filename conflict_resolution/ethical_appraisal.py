class EthicalAppraisal:
    def evaluate(self, action, context):
        if context.get("harm", False):
            return {"ethical": False, "reason": "harm"}
        return {"ethical": True}
