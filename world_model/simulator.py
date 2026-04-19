class Simulator:
    def __init__(self, world_state, causal_graph):
        self.world_state = world_state
        self.causal_graph = causal_graph

    def simulate_step(self, action):
        effects = self.causal_graph.get_effects(action)
        new_state = self.world_state.snapshot()

        # Update external entities based on causal effects
        for effect in effects:
            if effect in new_state["external"]["entities"]:
                # Simulation logic: increment entity property value if it exists
                entity = new_state["external"]["entities"][effect]
                if isinstance(entity, dict) and "value" in entity:
                    entity["value"] += 1
            else:
                # Add new entity if it's a discovered effect
                new_state["external"]["entities"][effect] = {"type": "inferred", "value": 1}

        return new_state

    def simulate_sequence(self, actions):
        state = self.world_state.snapshot()
        for action in actions:
            state = self.simulate_step(action)
        return state
