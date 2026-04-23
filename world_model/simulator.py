class Simulator:
    def __init__(self, world_state, causal_graph):
        self.state = world_state
        self.causal = causal_graph

    def simulate_action(self, action):
        # SGI 2026: Simulate action effects using causal graph
        current_state = self.state.snapshot()

        # Propagate effects
        effects = self.causal.propagate([action])

        # Apply effects to state (simplified)
        for effect in effects:
            if isinstance(effect, str) and "=" in effect:
                k, v = effect.split("=")
                current_state["external"][k] = v

        return current_state
