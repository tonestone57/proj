class IntrinsicRewardEngine:
    def __init__(self):
        self.weights = {
            "curiosity": 1.0,
            "uncertainty_reduction": 1.0,
            "novelty": 0.8,
            "goal_progress": 1.2
        }

    def compute(self, signals):
        # SGI 2026: Weighted intrinsic reward synthesis
        reward = 0.0
        applied_signals = {}

        for key, value in signals.items():
            weight = self.weights.get(key, 0.0)
            contribution = weight * value
            reward += contribution
            applied_signals[key] = contribution

        return {
            "total_intrinsic_reward": reward,
            "signal_contributions": applied_signals,
            "timestamp": time.time() if "time" in globals() else 0
        }
