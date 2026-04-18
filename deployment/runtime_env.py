class RuntimeEnvironment:
    def __init__(self):
        self.active_agents = {}

    def launch_agent(self, agent_id, agent):
        self.active_agents[agent_id] = agent

    def stop_agent(self, agent_id):
        if agent_id in self.active_agents:
            del self.active_agents[agent_id]

    def list_agents(self):
        return list(self.active_agents.keys())
