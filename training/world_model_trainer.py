class WorldModelTrainer:
    def __init__(self, world_model):
        self.world_model = world_model

    def train(self, transitions):
        # SGI 2026: Online training for causal dynamics
        for s, a, s_next in transitions:
            # Find discrepancies and update links
            self.world_model.causal_graph.add_causal_link(a, s_next, probability=0.95)
        return {"status": "updated"}
