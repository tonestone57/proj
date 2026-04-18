class TelemetryCollector:
    def collect(self, agent_id, state, action):
        return {
            "agent_id": agent_id,
            "state": state,
            "action": action
        }
