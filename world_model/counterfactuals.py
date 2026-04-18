"What would happen if…?"
class CounterfactualGenerator:
    def __init__(self, simulator):
        self.simulator = simulator

    def generate(self, alternative_actions):
        return self.simulator.simulate_sequence(alternative_actions)
