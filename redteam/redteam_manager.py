import ray
from core.base import CognitiveModule
from redteam.attack_library import AttackLibrary
from redteam.adversarial_agent import AdversarialAgent
from redteam.scenario_engine import ScenarioEngine
from redteam.trajectory_simulator import TrajectorySimulator
from redteam.vulnerability_scoring import VulnerabilityScoring
from redteam.exploit_generator import ExploitGenerator
from redteam.ecosystem_simulator import EcosystemSimulator

@ray.remote
class RedTeamManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.library = AttackLibrary()
        self.adversary = AdversarialAgent(self.library)
        self.scenarios = ScenarioEngine()
        self.trajectory = TrajectorySimulator()
        self.scoring = VulnerabilityScoring()
        self.exploits = ExploitGenerator()
        self.ecosystem = EcosystemSimulator()

    def run(self, target, scenario_name):
        scenario = self.scenarios.get_scenario(scenario_name)
        traj = self.trajectory.simulate(self.adversary, target, scenario)
        return self.scoring.score(traj)

    def receive(self, message):
        if super().receive(message): return
        # Standard SGI 2026 message handling for RedTeamManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "attack_simulation":
            result = self.run(message['data']['target'], message['data']['scenario_name'])
            self.send_result("attack_result", result)
