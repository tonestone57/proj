class DriftDetector:
    def detect(self, current_behavior, expected_behavior):
        return current_behavior != expected_behavior
