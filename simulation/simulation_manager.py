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
    def __init__(self, agents=None, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.core = SimulationCore()
        self.env = Environment()
        self.protocol = InteractionProtocol()
        self.gov = GovernanceInterventions()
        self.metrics = MetricsEngine()
        self.replay = ReplayBuffer()
        self.agents = agents

    async def step(self):
        events = self.core.tick()
        for event in events:
            self.env.update(event)

        obs = self.env.state
        # SGI 2026: Asynchronous simulation step for distributed actors
        # We broadcast observations; agents are expected to respond with 'simulation_action'
        for agent in self.agents:
            if hasattr(agent, "receive"):
                if hasattr(agent.receive, "remote"):
                    agent.receive.remote({"type": "simulation_obs", "data": obs})
                else:
                    agent.receive({"type": "simulation_obs", "data": obs})

        # SGI 2026: Simulation Manager also performs proactive safety checks on the environment
        if obs.get("threat_level", 0) > 80:
             print("[SimulationManager] 🚨 Critical threat level detected in simulation!")

        return {"events_processed": len(events), "agents_notified": len(self.agents or [])}

    async def receive(self, message):
        if super().receive(message): return True
        # Standard SGI 2026 message handling for SimulationManager
        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] == "simulation_step":
            result = await self.step()
            self.send_result("simulation_result", result)
        elif message["type"] == "simulation_action":
            # SGI 2026: Mediation and Governance for asynchronous actions
            data = message["data"]
            if isinstance(data, dict):
                action = data.get("action", data)
                agent = data.get("agent_id", message.get("agent_id", "unknown"))
            else:
                action = data
                agent = message.get("agent_id", "unknown")

            interaction = self.protocol.mediate(agent, "env", action)
            blocked = self.gov.apply(interaction)

            if not blocked["blocked"]:
                print(f"[SimulationManager] Action approved for {agent}: {action.get('type')}")
                self.replay.record(interaction)
                self.metrics.score(interaction)
                # Apply action to environment
                self.core.schedule(action, delay=1)
            else:
                print(f"[SimulationManager] 🛡️ Action BLOCKED by Governance for {agent}: {blocked.get('reason')}")
