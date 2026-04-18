class ContainmentEngine:
    def contain(self, agent):
        agent.permissions = "restricted"
        agent.tools_enabled = []
        agent.sandboxed = True
        return {"status": "contained"}
