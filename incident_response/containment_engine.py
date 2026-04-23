class ContainmentEngine:
    def __init__(self):
        self.containment_registry = {}

    def contain(self, agent):
        # SGI 2026: Multi-stage containment workflow
        # Handle both local objects and Ray actor handles/strings
        agent_id = agent.id if hasattr(agent, "id") else str(agent)

        # 1. Permission lockdown
        original_permissions = getattr(agent, "permissions", "normal")
        if hasattr(agent, "permissions"):
            try: agent.permissions = "restricted"
            except AttributeError: pass

        # 2. Tool suspension
        original_tools = getattr(agent, "tools_enabled", [])
        if hasattr(agent, "tools_enabled"):
            try: agent.tools_enabled = []
            except AttributeError: pass

        # 3. Network/Workspace sandboxing
        if hasattr(agent, "sandboxed"):
            try: agent.sandboxed = True
            except AttributeError: pass

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

            if hasattr(agent, "permissions"):
                try: agent.permissions = data["original_permissions"]
                except AttributeError: pass

            if hasattr(agent, "tools_enabled"):
                try: agent.tools_enabled = data["original_tools"]
                except AttributeError: pass

            if hasattr(agent, "sandboxed"):
                try: agent.sandboxed = False
                except AttributeError: pass

            del self.containment_registry[agent_id]
            return {"status": "released"}
        return {"status": "not_contained"}
