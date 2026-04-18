class MetaMonitor:
    def observe(self, internal_state, reasoning_trace):
        return {
            "state_snapshot": internal_state,
            "reasoning_trace": reasoning_trace,
            "anomalies": internal_state.get("anomalies", [])
        }
