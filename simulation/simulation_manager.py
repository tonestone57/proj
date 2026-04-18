from simulation.sim_core import SimulationCore
from simulation.environment import Environment
from simulation.interaction_protocol import InteractionProtocol
from simulation.governance_interventions import GovernanceInterventions
from simulation.metrics_engine import MetricsEngine
from simulation.replay_buffer import ReplayBuffer

class SimulationManager:
    def __init__(self, agents):
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
