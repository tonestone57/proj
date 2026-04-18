from world_model.state import WorldState
from world_model.causal_graph import CausalGraph
from world_model.simulator import Simulator
from world_model.prediction import PredictionEngine
from world_model.counterfactuals import CounterfactualGenerator

class WorldModelManager:
    def __init__(self):
        self.state = WorldState()
        self.causal_graph = CausalGraph()
        self.simulator = Simulator(self.state, self.causal_graph)
        self.predictor = PredictionEngine(self.simulator)
        self.counterfactuals = CounterfactualGenerator(self.simulator)

    def update_world(self, message):
        if message["type"] == "world_update":
            self.state.update_entity(message["entity"], message["data"])

        if message["type"] == "causal_update":
            self.causal_graph.add_causal_link(message["cause"], message["effect"])

    def predict_future(self, actions):
        return self.predictor.predict(actions)

    def imagine_alternative(self, actions):
        return self.counterfactuals.generate(actions)

from world_model.manager import WorldModelManager

world_model = WorldModelManager()
modules["world_model"] = world_model

if msg_type in ["world_update", "causal_update"]:
    return module_registry.get("world_model")
