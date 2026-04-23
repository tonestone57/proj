import psutil
import time

class TelemetryCollector:
    def collect(self, agent_id, state, action):
        # SGI 2026: Resource-aware telemetry collection
        mem = psutil.virtual_memory()

        return {
            "agent_id": agent_id,
            "timestamp": time.time(),
            "state": state,
            "action": action,
            "resources": {
                "cpu_percent": psutil.cpu_percent(),
                "mem_available_mb": mem.available / (1024 * 1024),
                "mem_percent": mem.percent
            }
        }
