import ray
from core.base import CognitiveModule

import re

@ray.remote # SGI 2026: Standardized Ray Actor
class DLPAgent(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.sensitive_patterns = {
            "api_key": r"(?:api|secret|token)_?(?:key|secret)?['\"]?\s*[:=]\s*['\"]?([a-zA-Z0-9]{32,})['\"]?",
            "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        }

    def inspect(self, data):
        data_str = str(data)
        leaks = []

        for name, pattern in self.sensitive_patterns.items():
            if re.search(pattern, data_str):
                leaks.append(name)

        if leaks or "sensitive" in data_str.lower():
            return {"leak_prevented": True, "detected_types": leaks}

        return {"leak_prevented": False}
