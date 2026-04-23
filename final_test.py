from core.model_registry import ModelRegistryBase
import ray

def test_registry():
    # Instantiate with mock search actor
    registry = ModelRegistryBase(search_actor=None)
    response = registry.generate("Hello SGI")
    print(f"Response: {response}")
    assert "Qwen3-8B" in response
    assert "Q4_K_M" in response

if __name__ == "__main__":
    test_registry()
