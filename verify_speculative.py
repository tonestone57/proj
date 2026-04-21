import sys
import os
import ray

# Ensure we can import from core
sys.path.append(os.getcwd())

# Mock ray if not running in a ray environment for simple verification
# But here we can just use ray.init if needed.
if not ray.is_initialized():
    ray.init(ignore_reinit_error=True)

def verify_speculative():
    print("--- Verifying Speculative Decoding ---")
    from core.model_registry import ModelRegistry

    registry = ModelRegistry.remote()

    # Test prose
    prose_prompt = "Hello, can you explain how quantum computing works in simple terms?"
    result_prose = ray.get(registry.generate.remote(prose_prompt))
    print(f"Prose Result thought block:\n{result_prose.split('</thought>')[0]}</thought>")
    assert "Neural Draft" in result_prose or "Neural speculation" in result_prose

    # Test code (syntax-heavy)
    code_prompt = "def calculate_fibonacci(n):\n    if n <= 1: return n\n    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)"
    result_code = ray.get(registry.generate.remote(code_prompt))
    print(f"Code Result thought block:\n{result_code.split('</thought>')[0]}</thought>")
    assert "N-Gram Lookahead" in result_code

    # Test N-Gram proposals
    ray.get(registry.update_ngram_cache.remote("def my_special_function(): return 42"))
    code_prompt_2 = "def my_special"
    result_code_2 = ray.get(registry.generate.remote(code_prompt_2))
    print(f"Code Result 2 thought block:\n{result_code_2.split('</thought>')[0]}</thought>")
    assert "N-Gram Lookahead" in result_code_2

    print("✅ Speculative Decoding verification complete.")

if __name__ == "__main__":
    verify_speculative()
    ray.shutdown()
