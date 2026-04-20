import ray
from core.base import CognitiveModule
from simulation.sim_core import SimulationCore
from simulation.environment import SimulatedEnvironment
from simulation.interaction_protocol import InteractionProtocol
from simulation.metrics_engine import SimulationMetrics
from simulation.agent_adapter import AgentAdapter
from simulation.governance_interventions import GovernanceInterventions
from simulation.replay_buffer import ReplayBuffer

@ray.remote
class SimulationManager(CognitiveModule):
    def __init__(self, agents=None, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.core = SimulationCore()
        self.env = SimulatedEnvironment()
        self.protocol = InteractionProtocol()
        self.metrics = SimulationMetrics()
        self.adapter = AgentAdapter(agents or [])
        self.interventions = GovernanceInterventions()
        self.replay = ReplayBuffer()

    def run_simulation(self, scenario, steps=100):
        state = self.env.reset(scenario)
        for _ in range(steps):
            actions = self.adapter.get_actions(state)
            next_state, results = self.core.step(state, actions)
            self.protocol.validate(results)
            self.interventions.apply(next_state)
            self.replay.store(state, actions, next_state)
            state = next_state
        return self.metrics.analyze(self.replay)

    def receive(self, message):
        # Standard SGI 2026 message handling for SimulationManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
