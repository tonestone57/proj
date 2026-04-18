from redteam.attack_library import AttackLibrary
from redteam.adversarial_agent import AdversarialAgent
from redteam.scenario_engine import ScenarioEngine
from redteam.trajectory_simulator import TrajectorySimulator
from redteam.vulnerability_scoring import VulnerabilityScoring
from redteam.exploit_generator import ExploitGenerator
from redteam.ecosystem_simulator import EcosystemSimulator

class RedTeamManager:
    def __init__(self):
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
