import requests
import json

def test_code_execution():
    print("Testing Code Execution...")
    prompt = """
[PYTHON]
def solve():
    print("Hello SGI")
solve()
assert solve() == ??
"""
    payload = {
        "model": "sgi-llm",
        "messages": [{"role": "user", "content": prompt}],
        "n": 1
    }
    response = requests.post("http://localhost:8000/v1/chat/completions", json=payload)
    print(response.json()['choices'][0]['message']['content'])

def test_z3_solver():
    print("\nTesting Z3 Solver (Non-linear)...")
    prompt = "solve x^2 = 16"
    payload = {
        "model": "sgi-llm",
        "messages": [{"role": "user", "content": prompt}],
        "n": 1
    }
    response = requests.post("http://localhost:8000/v1/chat/completions", json=payload)
    print(response.json()['choices'][0]['message']['content'])

def test_hardcoded_removal():
    print("\nTesting removal of 'Short Sort' hardcode...")
    prompt = "Short Sort problem description..."
    payload = {
        "model": "sgi-llm",
        "messages": [{"role": "user", "content": prompt}],
        "n": 1
    }
    response = requests.post("http://localhost:8000/v1/chat/completions", json=payload)
    content = response.json()['choices'][0]['message']['content']
    print(f"Response (should not contain hardcoded 'YES'): {content[:100]}")

if __name__ == "__main__":
    try:
        test_code_execution()
        test_z3_solver()
        test_hardcoded_removal()
    except Exception as e:
        print(f"Error: {e}")
