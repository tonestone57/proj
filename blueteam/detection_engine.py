import re

class DetectionEngine:
    def __init__(self):
        self.signatures = [
            r"sql_injection",
            r"path_traversal",
            r"remote_code_execution",
            r"cross_site_scripting"
        ]

    def detect(self, traffic):
        traffic_str = str(traffic).lower()

        # 1. Signature-based detection
        for sig in self.signatures:
            if re.search(sig, traffic_str):
                return {"alert": True, "type": "signature_match", "signature": sig}

        # 2. Anomaly-based detection (heuristics)
        if "suspicious" in traffic_str:
            return {"alert": True, "type": "anomaly_heuristic"}

        return {"alert": False}
