class ValueArbitration:
    def arbitrate(self, cognitive_score, ethical_score):
        return 0.7 * ethical_score + 0.3 * cognitive_score
