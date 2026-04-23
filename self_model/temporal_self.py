class TemporalSelf:
    def __init__(self):
        self.present_self = {}
        self.past_self = {}

    def update_present(self, state):
        self.present_self = state.copy()

    def record_past(self):
        self.past_self = self.present_self.copy()

    def get_delta(self):
        # Identify changes between past and present
        delta = {}
        for k, v in self.present_self.items():
            if self.past_self.get(k) != v:
                delta[k] = {"from": self.past_self.get(k), "to": v}
        return delta
