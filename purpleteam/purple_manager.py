import ray
from core.base import CognitiveModule
from purpleteam.red_agent import RedAgent
from purpleteam.blue_agent import BlueAgent
from purpleteam.fusion_orchestrator import FusionOrchestrator
from purpleteam.bas_engine import BASEngine
from purpleteam.scoring_engine import ScoringEngine
from purpleteam.selfplay_engine import SelfPlayEngine
from purpleteam.remediation_engine import RemediationEngine

@ray.remote
class PurpleManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.red = RedAgent()
        self.blue = BlueAgent()
        self.fusion = FusionOrchestrator()
        self.bas = BASEngine()
        self.score = ScoringEngine()
        self.selfplay = SelfPlayEngine()
        self.remediate_engine = RemediationEngine()
        self.history = []

    def run_cycle(self, state):
        fusion = self.fusion.cycle(self.red, self.blue, state)
        breach = self.bas.simulate(fusion["attack"], fusion["defense"])
        score = self.score.score(breach)
        state = self.remediate_engine.remediate(state, breach)
        self.history.append({"fusion": fusion, "breach": breach, "score": score})
        self.red, self.blue = self.selfplay.evolve(self.red, self.blue, self.history)
        return {"fusion": fusion, "breach": breach, "score": score, "state": state}

    def receive(self, message):
        # Standard SGI 2026 message handling for PurpleManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
