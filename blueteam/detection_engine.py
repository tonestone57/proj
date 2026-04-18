class DetectionEngine:
    def detect(self, traffic):
        if "suspicious" in traffic:
            return {"alert": True, "type": "anomaly"}
        return {"alert": False}
