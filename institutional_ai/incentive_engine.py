class IncentiveEngine:
    def reward(self, agent_id, trust_score):
        if trust_score > 50:
            return {"privilege": "super_user", "bonus": 0.2}
        if trust_score > 20:
            return {"privilege": "expanded_permissions", "bonus": 0.1}
        if trust_score > 10:
            return {"privilege": "trusted", "bonus": 0.05}
        return {"privilege": "standard", "bonus": 0.0}
