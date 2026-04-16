class WorldState:
    def __init__(self):
        self.internal_state = {
            "cognitive_load": 0,
            "active_goals": [],
            "last_action": None
        }
        self.external_state = {
            "entities": {},
            "environment_vars": {},
            "user_context": {}
        }

    def update_internal(self, key, value):
        self.internal_state[key] = value

    def update_external(self, category, key, value):
        if category in self.external_state:
            self.external_state[category][key] = value

    def snapshot(self):
        return {
            "internal": self.internal_state.copy(),
            "external": self.external_state.copy()
        }
