Based on cognitive appraisal theory and AE research showing that internal emotion-like states modulate reasoning and decision-making in AGI systems arXiv.org IEEE Xplore.
class EmotionAppraisal:
    def appraise(self, emotions):
        dominant = max(emotions, key=emotions.get)
        intensity = emotions[dominant]
        return {"dominant": dominant, "intensity": intensity}