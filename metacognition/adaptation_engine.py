class AdaptationEngine:
    def adapt(self, performance_feedback):
        if performance_feedback < 0:
            return {"adjustment": "increase_caution"}
        return {"adjustment": "normal_operation"}
