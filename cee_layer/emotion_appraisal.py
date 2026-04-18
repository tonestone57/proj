class EmotionAppraisal:
    def appraise(self, emotions):
        dominant = max(emotions, key=emotions.get)
        intensity = emotions[dominant]
        return {"dominant": dominant, "intensity": intensity}
