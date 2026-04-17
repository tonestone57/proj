Predicts future states.
class PredictionEngine:
    def __init__(self, simulator):
        self.simulator = simulator

    def predict(self, actions):
        return self.simulator.simulate_sequence(actions)
This is used by the planner and reasoning modules.