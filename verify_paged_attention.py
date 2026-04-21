import sys
import os
from unittest.mock import MagicMock, patch

# Ensure we can import from core
sys.path.append(os.getcwd())

def verify_paged_attention():
    print("--- Verifying PagedAttention Implementation ---")

    # Mock ray decorator to get the original class
    with patch("ray.remote", lambda x: x):
        with patch("ipex_llm.transformers.AutoModelForCausalLM.from_pretrained") as mock_load:
            mock_load.return_value = MagicMock()

            # Re-import to apply mock decorator
            if "core.model_registry" in sys.modules:
                del sys.modules["core.model_registry"]
            from core.model_registry import ModelRegistry

            registry = ModelRegistry(model_id="mock-model", draft_model_id="mock-draft")

            # Check if from_pretrained was called with use_paged_attention=True
            # It's called once for the main model
            found_paged = False
            for call in mock_load.call_args_list:
                _, kwargs = call
                if kwargs.get("use_paged_attention") is True:
                    found_paged = True
                    break

            assert found_paged, "use_paged_attention=True not found in any from_pretrained call"
            print("✅ PagedAttention flag verification complete.")

if __name__ == "__main__":
    # We need to mock the imports since they might not exist in the env
    with patch.dict(sys.modules, {
        "ipex_llm": MagicMock(),
        "ipex_llm.transformers": MagicMock()
    }):
        verify_paged_attention()
