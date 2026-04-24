import ray
from core.base import CognitiveModule
from cee_layer.emotion_generator import EmotionGenerator
from cee_layer.emotion_appraisal import EmotionAppraisal
from cee_layer.emotion_regulator import EmotionRegulator
from cee_layer.ethical_evaluator import EthicalEvaluator
from cee_layer.cognitive_affective_bridge import CognitiveAffectiveBridge
from cee_layer.moral_weighting import MoralWeighting

@ray.remote
class CEEManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
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

    def receive(self, message):
        if super().receive(message): return
        # Standard SGI 2026 message handling for CEEManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "stimulus_processing":
            result = self.process(message['data']['stimuli'], message['data']['reasoning_score'], message['data']['action'], message['data']['context'])
            self.send_result("stimulus_result", result)
