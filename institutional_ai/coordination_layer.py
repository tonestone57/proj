Implements AOM’s coordination architecture. California Management Review
class CoordinationLayer:
    def coordinate(self, agents, task):
        return {agent: task for agent in agents}