Computes individual and joint utilities.
class UtilitySystem:
    def individual(self, agent, proposal):
        return proposal.utility.get(agent, 0)

    def joint(self, agents, proposal):
        return sum(proposal.utility.get(a, 0) for a in agents)