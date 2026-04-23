import ray
from core.base import CognitiveModule
from world_model.state import WorldState
from world_model.causal_graph import CausalGraph
from world_model.simulator import Simulator
from world_model.prediction import PredictionEngine
from world_model.counterfactuals import CounterfactualGenerator

@ray.remote
class WorldModelManager(CognitiveModule):
    def __init__(self, workspace=None, scheduler=None, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.state = WorldState()
        self.causal_graph = CausalGraph()
        self.simulator = Simulator(self.state, self.causal_graph)
        self.predictor = PredictionEngine(self.simulator)
        self.counterfactuals = CounterfactualGenerator(self.simulator)

    def update_world(self, message):
        if message["type"] == "world_update":
            self.state.update_external("entities", message["entity"], message["data"])

        if message["type"] == "causal_update":
            self.causal_graph.add_causal_link(message["cause"], message["effect"])

    def predict_future(self, actions):
        return self.predictor.predict(actions)

    def imagine_alternative(self, actions):
        return self.counterfactuals.generate(actions)

    def update_entity(self, entity_id, data):
        # API used by ConsolidationManager
        self.state.update_external("entities", entity_id, data)

    def receive(self, message):
        try: super().receive(message)
        except NotImplementedError: pass
        # Standard SGI 2026 message handling for WorldModelManager

        print(f"[{self.__class__.__name__}] Received message: {message['type']}")
        if message["type"] in ["world_update", "causal_update"]:
            self.update_world(message)
        elif message["type"] == "prediction_request":
            result = self.predict_future(message['data']['actions'])
            self.send_result("prediction_result", result)