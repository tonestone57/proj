from core.model_registry import ModelRegistryBase
import unittest.mock as mock

def test_loading():
    # Force Stage 2 by mocking Stage 1 failure
    with mock.patch("ipex_llm.transformers.AutoModelForCausalLM.from_pretrained", side_effect=Exception("Direct IPEX Fail")):
        print("\n--- Testing Stage 2 Fallback (Standard Transformers + IPEX int8) ---")
        model_id = "hf-internal-testing/tiny-random-GPTNeoXForCausalLM"
        registry = ModelRegistryBase(model_id=model_id, draft_model_id=model_id)
        print(f"Status: {registry.get_model_info()}")

if __name__ == "__main__":
    test_loading()
