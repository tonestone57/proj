AIR (2026) emphasizes autonomous containment actions: tool disabling, sandboxing, permission reduction. arXiv.org
class ContainmentEngine:
    def contain(self, agent):
        agent.permissions = "restricted"
        agent.tools_enabled = []
        agent.sandboxed = True
        return {"status": "contained"}
This matches Microsoft’s safety-layer runtime guardrails. Microsoft Learn