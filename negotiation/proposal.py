class Proposal:
    def __init__(self, content, utility, agent_id):
        self.content = content
        self.utility = utility # Dict mapping agent_id -> utility value
        self.agent_id = agent_id

class ProposalEngine:
    def generate(self, agent, context):
        # SGI 2026: Reasoning-aware proposal generation
        # In a full implementation, this might call self.model_registry.generate
        # Mocking a proposal where the proposing agent gives it high utility (0.95)
        # and others get a base utility (0.5).
        return Proposal(f"Strategic Proposal from {agent} on {context}", {agent: 0.95}, agent)
