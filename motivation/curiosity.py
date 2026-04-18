class CuriosityModule:
    def __init__(self, world_model):
        self.world_model = world_model

    def compute_curiosity(self, action, predicted_state, actual_state):
        error = 0
        for key in predicted_state["properties"]:
            pred = predicted_state["properties"][key]
            act = actual_state["properties"].get(key, pred)
            error += abs(pred - act)
        return error
