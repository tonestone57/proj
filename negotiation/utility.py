class UtilityFunction:
    def __init__(self, role_weights):
        self.role_weights = role_weights

    def calculate(self, agent_id, proposal):
        # SGI 2026: Multi-objective utility calculation
        base_utility = proposal.utility.get(agent_id, 0.5)
        # Weight by role importance if applicable
        weight = self.role_weights.get(agent_id, 1.0)
        return min(1.0, base_utility * weight)
