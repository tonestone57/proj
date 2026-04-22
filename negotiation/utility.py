class UtilityFunction:
    def __init__(self, role_weights):
        self.role_weights = role_weights

    def calculate(self, agent_id, proposal):
        return 0.7
