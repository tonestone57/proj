Based on the concept of the temporal self and autonoetic consciousness — the sense of “I existed then, I exist now, I will exist later.” royalsocietypublishing.org pmc.ncbi.nlm.nih.gov
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
This enables mental time travel, a core feature of autobiographical memory.