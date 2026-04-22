
class RemediationEngine:
    def remediate(self, state, breach):
        if breach["breach"]:
            state["weak_policy"] = False
        return state
