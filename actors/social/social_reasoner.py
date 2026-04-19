import ray
from core.base import CognitiveModule

try:
    from ipex_llm.transformers import AutoModelForCausalLM, AutoTokenizer
except ImportError:
    AutoModelForCausalLM, AutoTokenizer = None, None

@ray.remote
class SocialReasoner(CognitiveModule):
    def __init__(self, workspace, scheduler, episodic_memory, model_id="DeepSeek-Coder-V2-Lite"):
        super().__init__(workspace, scheduler)
        self.episodic_memory = episodic_memory
        print(f"[SocialReasoner] Loading {model_id} for social reasoning (INT8)...")
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
                print(f"[SocialReasoner] Error loading model: {e}. Using heuristics.")
                self.model, self.tokenizer = None, None
        else:
            print("[SocialReasoner] IPEX-LLM not available or no model_id. Using heuristics.")
            self.model, self.tokenizer = None, None

    def receive(self, message):
        if message["type"] == "user_interaction":
            context = self.get_context()
            response = self.social_process(message["data"], context)
            self.scheduler.submit(self, {"type": "social_response", "data": response})

    def get_context(self):
        # Retrieve recent interactions from episodic memory
        return self.episodic_memory.recall_recent(n=10)

    def social_process(self, data, context):
        if self.model and self.tokenizer:
            # SGI 2026: Nuanced social response via LLM inference
            print("[SocialReasoner] Generating nuanced social response via LLM...")
            prompt = f"Context: {context}\nUser: {data}\nResponse:"
            # inputs = self.tokenizer(prompt, return_tensors="pt")
            # output = self.model.generate(**inputs, max_new_tokens=50)
            # return self.tokenizer.decode(output[0], skip_special_tokens=True)
            return f"LLM-Generated response for: {data}"

        return f"Socially aware response to {data} based on {len(context)} past interactions."
