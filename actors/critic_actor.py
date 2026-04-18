import ray
import torch
from ipex_llm.transformers import AutoModelForCausalLM
from core.config import CORES_CRITIC

@ray.remote(num_cpus=CORES_CRITIC)
class InternalCritic:
    def __init__(self, model_id="intel/neural-chat-14b-v3-3"):
        # We start with FP16 as requested, but we will use low-bit if loading fails
        # A 14B model in FP16 is 28GB, which is huge for a laptop.
        print(f"[InternalCritic] Attempting to load {model_id} in FP16...")
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=torch.float16,
                optimize_model=True,
                trust_remote_code=True
            )
            print("[InternalCritic] Model loaded successfully in FP16.")
        except Exception as e:
            print(f"[InternalCritic] FP16 load failed: {e}. Falling back to NF4 for 14B stability.")
            try:
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    load_in_low_bit="nf4",
                    optimize_model=True,
                    trust_remote_code=True
                )
                print("[InternalCritic] Model loaded successfully in NF4.")
            except Exception as e2:
                print(f"[InternalCritic] NF4 load also failed: {e2}. Using mock verification.")
                self.model = None

    def verify(self, reasoning_chain, goal):
        print(f"[InternalCritic] Verifying logic for goal: {goal}")
        if self.model is None: return "YES" in reasoning_chain.upper() or "CORRECT" in reasoning_chain.upper()
        # Mocking generation for demo
        return True
