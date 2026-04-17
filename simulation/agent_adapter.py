Ensures strict separation of agent logic vs. environment dynamics.
api.emergentmind.com
class AgentAdapter:
    def __init__(self, agent):
        self.agent = agent

    def step(self, observation):
        return self.agent.act(observation)