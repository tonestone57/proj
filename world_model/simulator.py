Runs forward simulations based on the world state + causal graph.
class Simulator:
    def __init__(self, world_state, causal_graph):
        self.world_state = world_state
        self.causal_graph = causal_graph

    def simulate_step(self, action):
        effects = self.causal_graph.get_effects(action)
        new_state = self.world_state.snapshot()

        for effect in effects:
            if effect in new_state["properties"]:
                new_state["properties"][effect] += 1

        return new_state

    def simulate_sequence(self, actions):
        state = self.world_state.snapshot()
        for action in actions:
            state = self.simulate_step(action)
        return state
This is the AGI’s internal physics + logic engine.