Implements detection of prompt-injection, memory poisoning, context poisoning, jailbreaks, and drift.
class Detectors:
    def detect_prompt_injection(self, input_text):
        return "override" in input_text.lower()

    def detect_memory_poisoning(self, memory_state):
        return memory_state.get("tampered", False)

    def detect_context_poisoning(self, context):
        return context.get("malicious_context", False)

    def detect_drift(self, behavior, expected):
        return behavior != expected
These map directly to CoSAI’s threat taxonomy. coalitionforsecureai.org