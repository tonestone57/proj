import math

class CuriosityModule:
    def __init__(self, world_model):
        self.world_model = world_model
        self.surprise_history = []

    def compute_curiosity(self, action, predicted_state, actual_state):
        # SGI 2026: Curiosity based on Prediction Error (Surprise)
        error = 0

        # Handle cases where state might be complex dicts
        pred_props = predicted_state.get("properties", predicted_state)
        act_props = actual_state.get("properties", actual_state)

        if not isinstance(pred_props, dict): return 0.1 # Baseline

        for key, pred in pred_props.items():
            if isinstance(pred, (int, float)):
                act = act_props.get(key, pred)
                error += (pred - act) ** 2

        surprise = math.sqrt(error)
        self.surprise_history.append(surprise)

        # SGI Curiosity Drive: normalized surprise
        return min(1.0, surprise / 10.0)

    def get_avg_surprise(self):
        if not self.surprise_history: return 0.0
        return sum(self.surprise_history) / len(self.surprise_history)
