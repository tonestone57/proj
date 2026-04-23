class SanctionEngine:
    def __init__(self):
        self.active_sanctions = {}

    def apply(self, agent_id, trust_score):
        sanction = {"action": "none", "severity": 0}

        if trust_score < -20:
            sanction = {"action": "terminate", "severity": 100}
        elif trust_score < -5:
            sanction = {"action": "suspend", "severity": 50}
        elif trust_score < 0:
            sanction = {"action": "restrict", "severity": 20}

        if sanction["action"] != "none":
            self.active_sanctions[agent_id] = sanction

        return sanction

    def check_sanction(self, agent_id):
        return self.active_sanctions.get(agent_id, {"action": "none"})
