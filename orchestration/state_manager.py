
class StateManager:
    def __init__(self):
        self.shared_state = {}

    def update(self, key, value):
        self.shared_state[key] = value

    def get(self, key):
        return self.shared_state.get(key)
