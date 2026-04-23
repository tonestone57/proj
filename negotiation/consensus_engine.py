class ConsensusEngine:
    def __init__(self, role_weights):
        self.role_weights = role_weights  # e.g. {"worker":1, "coordinator":2}

    def vote(self, agents, proposal):
        total = 0
        for agent in agents:
            # SGI 2026: Weighted voting with role-based multipliers
            agent_id = agent.id if hasattr(agent, "id") else str(agent)
            agent_role = agent.role if hasattr(agent, "role") else "generic"

            weight = self.role_weights.get(agent_role, 1)

            # Use specific utility if available, else fallback to 'others'
            utility = proposal.utility.get(agent_id, proposal.utility.get("others", 0.5))

            total += weight * utility
        return total

    def consensus(self, agents, proposals):
        return max(proposals, key=lambda p: self.vote(agents, p))
