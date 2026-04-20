class TrustEngine:
    def __init__(self):
        self.scores = {}

    def update(self, agent_id, compliant):
        self.scores.setdefault(agent_id, 0)
        self.scores[agent_id] += 1 if compliant else -2

    def get_score(self, agent_id):
        return self.scores.get(agent_id, 0)
