class Proposal:
    def __init__(self, content, utility, agent_id):
        self.content = content
        self.utility = utility
        self.agent_id = agent_id

class ProposalEngine:
    def generate(self, agent, context):
        return Proposal(f"Proposal from {agent}", 0.8, agent)
