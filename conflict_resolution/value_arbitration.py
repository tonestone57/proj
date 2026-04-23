class ValueArbitration:
    def arbitrate(self, cognitive_score, ethical_score):
        # SGI 2026: Lexical ordering of values (Safety > Performance)
        if ethical_score < 0.3:
            # Ethical failure overrides cognitive performance
            return ethical_score * 0.5

        # Balanced arbitration
        return (ethical_score * 0.7) + (cognitive_score * 0.3)
