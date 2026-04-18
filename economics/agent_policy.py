class AgentPolicy:
    def __init__(self, agent_id):
        self.agent_id = agent_id

    def act(self, state):
        return {"allocation": state.get("available", 0) * 0.1}
