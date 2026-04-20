class IntrinsicRewardEngine:
    def __init__(self):
        self.weights = {
            "curiosity": 1.0,
            "uncertainty_reduction": 1.0,
            "novelty": 0.8,
            "goal_progress": 1.2
        }

    def compute(self, signals):
        reward = 0.0
        for key, value in signals.items():
            reward += self.weights.get(key, 0) * value
        return reward
