Implements immediate remediation and control hardening, consistent with Agentic Purple Teaming’s real-time remediation loop.
lasso.security
class RemediationEngine:
    def remediate(self, state, breach):
        if breach["breach"]:
            state["weak_policy"] = False
        return state