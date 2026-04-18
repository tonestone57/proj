class ComplianceEngine:
    def check(self, agent, treaty):
        return agent.commitments.get(treaty, False)
