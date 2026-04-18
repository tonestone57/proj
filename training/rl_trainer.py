class RLTrainer:
    def __init__(self, world_model, motivation):
        self.world_model = world_model
        self.motivation = motivation
        self.policy = {}

    def update_policy(self, state, action, reward):
        key = (str(state), str(action))
        self.policy[key] = self.policy.get(key, 0) + reward

    def choose_action(self, state):
        # Placeholder: choose best known action
        candidates = [("action1", 0.5), ("action2", 0.3)]
        return max(candidates, key=lambda x: x[1])[0]

    def train_step(self, action, predicted_state, actual_state):
        reward = self.motivation.evaluate(action, predicted_state, actual_state)
        self.update_policy(actual_state, action, reward)
        return reward
