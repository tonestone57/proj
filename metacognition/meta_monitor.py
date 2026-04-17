Implements the Nelson–Narens meta-level → object-level monitoring architecture (core cognitive science model).
This is the meta-level reading the object-level.
class MetaMonitor:
    def observe(self, internal_state, reasoning_trace):
        return {
            "state_snapshot": internal_state,
            "reasoning_trace": reasoning_trace,
            "anomalies": internal_state.get("anomalies", [])
        }
This provides self-observation, a key metacognitive function.
zylos.ai