class TemporalSelf:
    def __init__(self):
        self.past_self = {}
        self.present_self = {}
        self.future_projection = {}

    def update_present(self, state):
        self.present_self = state

    def record_past(self):
        self.past_self = self.present_self.copy()

    def project_future(self, goals):
        self.future_projection = {"goals": goals, "expected_state": self.present_self}
        return self.future_projection
