class CounterfactualGenerator:
    def __init__(self, simulator):
        self.simulator = simulator

    def generate(self, actions):
        # SGI 2026: "What-if" reasoning
        alternatives = []
        for action in actions:
            alternative_action = f"not_{action}"
            outcome = self.simulator.simulate_action(alternative_action)
            alternatives.append({"original": action, "alternative": alternative_action, "outcome": outcome})
        return alternatives
