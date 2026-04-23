import collections

class TrustEngine:
    def __init__(self):
        self.scores = {}
        self.history = collections.defaultdict(list)
        self.config = {
            "compliant_bonus": 1,
            "violation_penalty": -3,
            "max_score": 100,
            "min_score": -50
        }

    def update(self, agent_id, compliant, context=None):
        self.scores.setdefault(agent_id, 10) # Start with base trust

        delta = self.config["compliant_bonus"] if compliant else self.config["violation_penalty"]

        # Apply context-based multipliers if needed
        if context and context.get("high_stakes"):
            delta *= 2

        self.scores[agent_id] = max(self.config["min_score"],
                                   min(self.config["max_score"],
                                       self.scores[agent_id] + delta))

        self.history[agent_id].append({
            "delta": delta,
            "score": self.scores[agent_id],
            "compliant": compliant,
            "context": context
        })

    def get_score(self, agent_id):
        return self.scores.get(agent_id, 10)

    def get_history(self, agent_id):
        return self.history.get(agent_id, [])
