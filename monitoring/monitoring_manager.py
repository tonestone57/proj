from monitoring.telemetry_collector import TelemetryCollector
from monitoring.semantic_trace import SemanticTrace
from monitoring.drift_detector import DriftDetector
from monitoring.conformance_engine import ConformanceEngine
from monitoring.risk_monitor import RiskMonitor

class MonitoringManager:
    def __init__(self):
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
