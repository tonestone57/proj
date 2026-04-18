class Optimizer:
    def optimize(self, agents, state):
        proposals = [a.act(state)["allocation"] for a in agents]
        return proposals
