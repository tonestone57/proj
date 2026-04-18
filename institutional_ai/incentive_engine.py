class IncentiveEngine:
    def reward(self, agent_id, trust_score):
        if trust_score > 10:
            return {"privilege": "expanded_permissions"}
        return {"privilege": "standard"}
