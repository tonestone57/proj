import time
import ray
from core.base import CognitiveModule

@ray.remote
class MetaMonitor(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.performance_history = []

    def observe(self, internal_state, reasoning_trace):
        # SGI 2026: Calculate cognitive efficiency
        trace_len = len(str(reasoning_trace))
        latency = internal_state.get("latency", 0.0)

        # Efficiency is trace length per unit of latency (simulated)
        efficiency = trace_len / (latency + 0.001)

        observation = {
            "timestamp": time.time(),
            "state_snapshot": internal_state,
            "reasoning_trace": reasoning_trace,
            "anomalies": internal_state.get("anomalies", []),
            "metrics": {
                "efficiency": efficiency,
                "entropy": internal_state.get("entropy", 0.0),
                "throughput": trace_len
            }
        }

        self.performance_history.append(observation)
        if len(self.performance_history) > 100:
            self.performance_history.pop(0)

        return observation

    def get_aggregate_metrics(self):
        if not self.performance_history:
            return {}

        avg_efficiency = sum(o["metrics"]["efficiency"] for o in self.performance_history) / len(self.performance_history)
        return {
            "average_efficiency": avg_efficiency,
            "observation_count": len(self.performance_history)
        }
