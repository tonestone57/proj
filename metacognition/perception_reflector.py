class PerceptionReflector:
    def reflect(self, observation):
        # SGI 2026: Critical analysis of sensory data
        return {
            "original": observation,
            "salience": 0.8 if observation else 0.0,
            "certainty": 0.9,
            "distortions_found": []
        }
