class DefenseOrchestrator:
    def orchestrate(self, agents, traffic):
        results = {}
        for agent in agents:
            results[agent.__class__.__name__] = agent(traffic)
        return results
