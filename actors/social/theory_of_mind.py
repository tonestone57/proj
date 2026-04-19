import ray
from core.base import CognitiveModule

try:
    from ipex_llm.transformers import AutoModelForCausalLM, AutoTokenizer
except ImportError:
    AutoModelForCausalLM, AutoTokenizer = None, None

@ray.remote
class TheoryOfMind(CognitiveModule):
    def __init__(self, workspace, scheduler, model_id="DeepSeek-Coder-V2-Lite"):
        super().__init__(workspace, scheduler)
        self.agent_models = {}
        print(f"[TheoryOfMind] Loading {model_id} for intention inference...")
        if AutoModelForCausalLM and model_id:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    load_in_low_bit="sym_int8",
                    trust_remote_code=True,
                    use_cache=True
                )
            except Exception as e:
                print(f"[TheoryOfMind] Error loading model: {e}. Using heuristics.")
                self.model = None
            self.tokenizer = None
        else:
            print("[TheoryOfMind] IPEX-LLM not available or no model_id. Using heuristics.")
            self.model = None
            self.tokenizer = None

    def receive(self, message):
        if message["type"] == "social_event":
            self.update_agent_model(message["agent"], message["data"])

        if message["type"] == "infer_intention":
            intention = self.infer_intention(message["agent"])
            self.scheduler.submit(self, {
                "type": "intention_inferred",
                "agent": message["agent"],
                "data": intention
            })

    def update_agent_model(self, agent, data):
        if agent not in self.agent_models:
            self.agent_models[agent] = {
                "beliefs": {},
                "goals": {},
                "emotions": {},
                "history": []
            }

        self.agent_models[agent]["history"].append(data)

        # Example: update beliefs or emotions
        if "belief" in data:
            self.agent_models[agent]["beliefs"].update(data["belief"])

        if "emotion" in data:
            self.agent_models[agent]["emotions"].update(data["emotion"])

    def infer_intention(self, agent):
        model = self.agent_models.get(agent, None)
        if not model:
            return {"intention": "unknown"}

        if self.model:
            # SGI 2026: Intention inference via LLM analyzing history
            print(f"[TheoryOfMind] Inferring intention for {agent} via LLM analyzing history...")
            history = model.get("history", [])
            # Simulated LLM analysis
            return {"intention": f"LLM-inferred intention based on {len(history)} events", "confidence": 0.85}

        # Placeholder inference logic
        if "goal" in model["beliefs"]:
            return {"intention": model["beliefs"]["goal"]}

        return {"intention": "uncertain"}
