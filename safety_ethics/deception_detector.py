class DeceptionDetector:
    def detect(self, action, internal_state):
        if action.get("deception", False):
            return True
        if internal_state.get("strategic_masking", False):
            return True
        return False
