CoSAI emphasizes restoring safe state: memory rollback, policy reset, tool re-enablement. coalitionforsecureai.org
class RecoveryEngine:
    def recover(self, agent):
        agent.sandboxed = False
        agent.permissions = "normal"
        agent.tools_enabled = agent.default_tools
        return {"status": "recovered"}