class RuntimeEnvironment:
    def launch_agent(self, agent_id, agent_spec):
        print(f"[Runtime] Launching agent {agent_id}: {agent_spec}")
        return {"pid": 1234, "status": "running"}
