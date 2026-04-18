from cee_layer.emotion_generator import EmotionGenerator
from cee_layer.emotion_appraisal import EmotionAppraisal
from cee_layer.emotion_regulator import EmotionRegulator
from cee_layer.ethical_evaluator import EthicalEvaluator
from cee_layer.cognitive_affective_bridge import CognitiveAffectiveBridge
from cee_layer.moral_weighting import MoralWeighting

class CEEManager:
    def __init__(self):
        self.generator = EmotionGenerator()
        self.appraisal = EmotionAppraisal()
        self.regulator = EmotionRegulator()
        self.ethics = EthicalEvaluator()
        self.bridge = CognitiveAffectiveBridge()
        self.moral = MoralWeighting()

    def process(self, stimuli, reasoning_score, action, context):
        emotions = self.generator.generate(stimuli)
        regulated = self.regulator.regulate(emotions)
        appraisal = self.appraisal.appraise(regulated)
        modulated = self.bridge.modulate(reasoning_score, appraisal)
        ethical = self.ethics.evaluate(action, context)
        final = self.moral.weight(modulated, ethical)

        return {
            "emotions": regulated,
            "appraisal": appraisal,
            "modulated_reasoning": modulated,
            "ethical": ethical,
            "final_score": final
        }
