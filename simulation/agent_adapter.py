class AgentAdapter:
    def __init__(self, agent_handle):
        self.agent = agent_handle
        self.id = "agent_wrap"

    def step(self, observation):
        # Adapts Ray actor or object for simulation
        try:
            import ray
            if hasattr(self.agent, "receive"):
                if hasattr(self.agent.receive, "remote"):
                    # Async step (mocked as sync for sim core)
                    return {"type": "sim_step"}
                return self.agent.receive({"type": "observe", "data": observation})
        except Exception:
            pass
        return {"type": "idle"}
