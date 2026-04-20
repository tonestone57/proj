import ray
from core.base import CognitiveModule
from simulation.sim_core import SimulationCore
from simulation.environment import Environment
from simulation.interaction_protocol import InteractionProtocol
from simulation.governance_interventions import GovernanceInterventions
from simulation.metrics_engine import MetricsEngine
from simulation.replay_buffer import ReplayBuffer

@ray.remote
class SimulationManager(CognitiveModule):
    def __init__(self, agents, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.core = SimulationCore()
        self.env = Environment()
        self.protocol = InteractionProtocol()
        self.gov = GovernanceInterventions()
        self.metrics = MetricsEngine()
        self.replay = ReplayBuffer()
        self.agents = agents

    def step(self):
        event = self.core.tick()
        if event:
            self.env.update(event)

        for agent in self.agents:
            obs = self.env.state
            action = agent.step(obs)
            interaction = self.protocol.mediate(agent, "env", action)
            blocked = self.gov.apply(interaction)
            if not blocked["blocked"]:
                self.replay.record(interaction)
                self.metrics.score(interaction)

# OK: What you now have

    def receive(self, message):
        # Standard SGI 2026 message handling for SimulationManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
