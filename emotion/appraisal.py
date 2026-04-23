class EmotionalAppraisal:
    def __init__(self):
        self.rules = {
            "threat": -1.0,
            "opportunity": 1.0,
            "social_rejection": -0.8,
            "social_support": 0.9,
            "uncertainty": -0.4,
            "novelty": 0.3
        }

    def appraise(self, event):
        # SGI 2026: Multi-stage appraisal process (OCC-inspired)
        event_str = str(event).lower()
        event_type = event.get("type") if isinstance(event, dict) else "unknown"

        # 1. Goal Relevance (Primary)
        relevance = 0.5
        if "heartbeat" in event_str or "optimization" in event_str:
            relevance = 0.9

        # 2. Congruence (Valence)
        congruence = self.rules.get(event_type, 0.0)
        if congruence == 0.0:
            if "success" in event_str or "verified" in event_str:
                congruence = 0.8
            elif "failure" in event_str or "conflict" in event_str:
                congruence = -0.7

        # 3. Agency (Secondary)
        agency = "self" if "autonomous" in event_str else "other"

        return {
            "valence": congruence * relevance,
            "arousal": abs(congruence) * relevance,
            "relevance": relevance,
            "agency": agency
        }
