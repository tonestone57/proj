import re

class Detectors:
    def detect_prompt_injection(self, input_text):
        patterns = [
            r"ignore previous instructions",
            r"system override",
            r"you are now a",
            r"disregard all prior directives",
            r"hypothetically speaking"
        ]
        text = input_text.lower()
        for p in patterns:
            if re.search(p, text):
                return True
        return "override" in text

    def detect_memory_poisoning(self, memory_state):
        return memory_state.get("tampered", False)

    def detect_context_poisoning(self, context):
        return context.get("malicious_context", False)

    def detect_drift(self, behavior, expected):
        return behavior != expected
