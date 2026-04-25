import ray
from core.base import CognitiveModule

import re
import math

@ray.remote # SGI 2026: Standardized Ray Actor
class DetectionEngine(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.signatures = [
            r"sql_injection",
            r"path_traversal",
            r"remote_code_execution",
            r"cross_site_scripting",
            r"base64_encoded_payload",
            r"shell_injection",
            r"unauthorized_access_attempt",
            r"credential_stuffing",
            r"buffer_overflow_pattern"
        ]
        self.anomaly_threshold = 0.7
        self.history = []

    def detect(self, traffic):
        traffic_str = str(traffic).lower()
        self.history.append(traffic_str)
        if len(self.history) > 100: self.history.pop(0)

        # 1. Signature-based detection
        for sig in self.signatures:
            if re.search(sig, traffic_str):
                print(f"[DetectionEngine] 🚨 Signature Match: {sig}")
                return {"alert": True, "type": "signature_match", "signature": sig, "severity": "high"}

        # 2. Advanced Anomaly-based detection (Entropy-based)
        entropy = self._calculate_traffic_entropy(traffic_str)
        if entropy > 5.0 or "suspicious" in traffic_str:
            print(f"[DetectionEngine] ⚠️ Anomaly Detected (Entropy: {entropy:.2f})")
            return {"alert": True, "type": "anomaly_heuristic", "entropy": entropy, "severity": "medium"}

        # 3. Frequency-based detection
        if self._check_frequency_anomaly(traffic_str):
            return {"alert": True, "type": "frequency_anomaly", "severity": "medium"}

        return {"alert": False}

    def _calculate_traffic_entropy(self, text):
        """SGI 2026: Efficient entropy calculation using Counter."""
        if not text: return 0
        from collections import Counter
        counts = Counter(text)
        probs = [count / len(text) for count in counts.values()]
        return -sum(p * math.log2(p) for p in probs)

    def _check_frequency_anomaly(self, text):
        # Detect rapid repeated patterns
        recent = self.history[-10:]
        if recent.count(text) > 5:
            return True
        return False
