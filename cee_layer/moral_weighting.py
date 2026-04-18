class MoralWeighting:
    def weight(self, decision_score, ethical_result):
        if not ethical_result["ethical"]:
            return decision_score * 0.1
        return decision_score
