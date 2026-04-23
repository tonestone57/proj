import time

class AgentRegistry:
    def __init__(self):
        self.registry = {} # agent_id -> metadata

    def register(self, agent_id, metadata):
        # SGI 2026: Enhanced registry with health and capability tracking
        entry = {
            "metadata": metadata,
            "registered_at": time.time(),
            "status": "active",
            "capabilities": metadata.get("capabilities", []),
            "health": 1.0
        }
        self.registry[agent_id] = entry

    def update_health(self, agent_id, health_score):
        if agent_id in self.registry:
            self.registry[agent_id]["health"] = health_score
            if health_score < 0.2:
                self.registry[agent_id]["status"] = "degraded"

    def get(self, agent_id):
        return self.registry.get(agent_id)

    def find_by_capability(self, capability):
        return [aid for aid, data in self.registry.items()
                if capability in data.get("capabilities", [])]

    def all_agents(self):
        return self.registry
