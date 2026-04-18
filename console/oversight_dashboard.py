Deloitte
class OversightDashboard:
    def __init__(self):
        self.metrics = {}

    def update(self, agent_name, data):
        self.metrics[agent_name] = data

    def view(self):
        return self.metrics
