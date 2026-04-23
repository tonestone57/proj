import ray
from core.base import CognitiveModule
from monitoring.telemetry_collector import TelemetryCollector
from monitoring.semantic_trace import SemanticTrace
from monitoring.drift_detector import DriftDetector
from monitoring.conformance_engine import ConformanceEngine
from monitoring.risk_monitor import RiskMonitor

@ray.remote
class MonitoringManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.telemetry = TelemetryCollector()
        self.trace = SemanticTrace()
        self.drift = DriftDetector()
        self.conformance = ConformanceEngine()
        self.risk = RiskMonitor()

    def monitor(self, agent_id, state, action, reasoning, allowed_actions):
        t = self.telemetry.collect(agent_id, state, action)
        trace = self.trace.trace(reasoning)
        drift = self.drift.detect(action, allowed_actions)
        conformance = self.conformance.check(action, allowed_actions)
        risk = self.risk.assess(t)

        return {
            "telemetry": t,
            "trace": trace,
            "drift": drift,
            "conformance": conformance,
            "risk": risk
        }

    def receive(self, message):
        try: super().receive(message)
        except NotImplementedError: pass
        # Standard SGI 2026 message handling for MonitoringManager

        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "monitoring_request":
            result = self.monitor(message['data']['agent_id'], message['data']['state'], message['data']['action'], message['data']['reasoning'], message['data']['allowed_actions'])
            self.send_result("monitoring_result", result)