class ContainmentEngine:
    def __init__(self):
        self.containment_registry = {}

    def contain(self, agent):
        # SGI 2026: Multi-stage containment workflow
        agent_id = agent.id if hasattr(agent, "id") else str(agent)

        # 1. Permission lockdown
        original_permissions = getattr(agent, "permissions", "normal")
        agent.permissions = "restricted"

        # 2. Tool suspension
        original_tools = getattr(agent, "tools_enabled", [])
        agent.tools_enabled = []

        # 3. Network/Workspace sandboxing
        agent.sandboxed = True

        self.containment_registry[agent_id] = {
            "original_permissions": original_permissions,
            "original_tools": original_tools,
            "status": "contained"
        }

        return {"status": "contained", "level": "high_isolation"}

    def release(self, agent):
        agent_id = agent.id if hasattr(agent, "id") else str(agent)
        if agent_id in self.containment_registry:
            data = self.containment_registry[agent_id]
            agent.permissions = data["original_permissions"]
            agent.tools_enabled = data["original_tools"]
            agent.sandboxed = False
            del self.containment_registry[agent_id]
            return {"status": "released"}
        return {"status": "not_contained"}
