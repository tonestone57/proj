class StrategyOptimizer:
    def __init__(self):
        self.strategy_scores = {}

    def update(self, strategy, reward):
        if strategy not in self.strategy_scores:
            self.strategy_scores[strategy] = 0
        self.strategy_scores[strategy] += reward

    def best_strategy(self):
        if not self.strategy_scores:
            return None
        return max(self.strategy_scores.items(), key=lambda x: x[1])[0]
