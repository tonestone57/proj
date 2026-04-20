class PredictionEngine:
    def __init__(self, simulator):
        self.simulator = simulator

    def predict(self, actions):
        return self.simulator.simulate_sequence(actions)
