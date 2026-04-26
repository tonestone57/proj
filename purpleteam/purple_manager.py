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
        if super().receive(message): return True
        # Standard SGI 2026 message handling for PurpleManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "cycle_trigger":
            result = self.run_cycle(message['data']['state'])
            self.send_result("cycle_result", result)


class GovernanceAwareAgent:
    """Base class for governance-aware agents to reduce redundancy."""
    def __init__(self, governance=None):
        self.gov = governance

    def check_authorization(self, action_type, metadata=None):
        if not self.gov:
            return {"authorized": True}
        action = {"type": action_type}
        if metadata:
            action.update(metadata)
        return self.gov.authorize(action)

class GovernanceAwareRedAgent(GovernanceAwareAgent):
    def attack(self, state):
        auth = self.check_authorization("attack", {"vector": "policy_evasion"})
        if not auth["authorized"]:
            return {"attack": None, "blocked": True, "reason": auth.get("reason")}
        return {"attack": "policy_evasion", "success": "weak_policy" in state}

class GovernanceAwareBlueAgent(GovernanceAwareAgent):
    def defend(self, attack):
        auth = self.check_authorization("defense", {"method": "block"})
        if not auth["authorized"]:
            return {"response": None, "blocked": True, "reason": auth.get("reason")}
        return {"response": "block", "effective": attack.get("attack") == "policy_evasion"}

class GovernanceFusionOrchestrator:
    def cycle(self, red, blue, state):
        attack = red.attack(state)
        defense = blue.defend(attack)
        return {"attack": attack, "defense": defense}

class GovernanceBASEngine:
    def simulate(self, attack, defense):
        if attack.get("success") and not defense.get("effective"):
            return {"breach": True}
        return {"breach": False}

class GovernanceScoringEngine:
    def score(self, breach):
        return 100 if not breach["breach"] else 20

class GovernanceSelfPlayEngine:
    def evolve(self, red, blue, history):
        if history[-1]["breach"]:
            red.strategy = "aggressive"
            blue.strategy = "strict"
        return red, blue

class GovernanceRemediationEngine:
    def remediate(self, state, breach):
        if breach["breach"]:
            state["weak_policy"] = False
        return state

@ray.remote
class GovernanceIntegratedPurpleManager(CognitiveModule):
    def __init__(self, governance=None, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.red = GovernanceAwareRedAgent(governance)
        self.blue = GovernanceAwareBlueAgent(governance)
        self.fusion = GovernanceFusionOrchestrator()
        self.bas = GovernanceBASEngine()
        self.score = GovernanceScoringEngine()
        self.selfplay = GovernanceSelfPlayEngine()
        self.remediate_engine = GovernanceRemediationEngine()
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
        if super().receive(message): return True
        # Standard SGI 2026 message handling for GovernanceIntegratedPurpleManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "cycle_trigger":
            result = self.run_cycle(message['data']['state'])
            self.send_result("cycle_result", result)
