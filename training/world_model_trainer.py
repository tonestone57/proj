class WorldModelTrainer:
    def __init__(self, world_model):
        self.world_model = world_model

    def train_step(self, action, actual_state):
        # Update causal graph or state based on new data
        self.world_model.state.entities.update(actual_state["entities"])
        return True
