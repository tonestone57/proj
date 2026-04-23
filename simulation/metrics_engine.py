class MetricsEngine:
    def __init__(self):
        self.stats = {"interactions": 0, "total_reward": 0.0}

    def score(self, interaction):
        self.stats["interactions"] += 1
        # Simple heuristic scoring
        if interaction.get("action", {}).get("type") == "cooperate":
            self.stats["total_reward"] += 1.0

    def get_report(self):
        return self.stats
