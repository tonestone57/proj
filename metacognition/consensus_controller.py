class ConsensusController:
    def combine(self, monitor_report, reasoner_report):
        issues = monitor_report["anomalies"] + reasoner_report["issues"]
        if issues:
            return {"status": "alert", "issues": issues}
        return {"status": "stable"}
