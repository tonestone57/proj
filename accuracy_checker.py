import sys
import os
import ray
import re

# Add current directory to path for imports
sys.path.append(os.getcwd())

from core.workspace import GlobalWorkspace
from core.scheduler import Scheduler
from actors.search_actor import SearchActor

def calculate_mrr(results, ground_truth):
    """
    Calculates Reciprocal Rank for a single query.
    results: List of ranked document strings.
    ground_truth: The target document string that should be at the top.
    """
    for i, res in enumerate(results):
        if ground_truth in str(res):
            return 1.0 / (i + 1)
    return 0.0

def run_benchmark():
    print("--- SGI-Alpha Search Accuracy Benchmark (Reranker MRR) ---")

    # Define ground truth test cases based on SGI 2026 specifications
    test_cases = [
        {
            "query": "AVX2 optimization for sym_int8",
            "ground_truth": "AVX2 optimization requires 32-byte alignment and sym_int8 precision removes zero-point offsets.",
            "candidates": [
                "Forum: How do I use AVX2? I think it's fast.",
                "StackOverflow: AVX2 vs SSE4.2 performance comparison on Whiskey Lake.",
                "AVX2 optimization requires 32-byte alignment and sym_int8 precision removes zero-point offsets.",
                "Random text about Intel CPUs and thermal throttling.",
                "Discussion on how sym_int8 is better than float32 for reasoning."
            ]
        },
        {
            "query": "SGI 2026 compression standards",
            "ground_truth": "SGI 2026 utilizes Q4_K_M for weights, sym_int8 for reasoning, and LLM-Zip for deep archiving.",
            "candidates": [
                "Standard Zstd compression is good for logs.",
                "SGI 2026 utilizes Q4_K_M for weights, sym_int8 for reasoning, and LLM-Zip for deep archiving.",
                "Forum: Does anyone know the new SGI compression specs?",
                "Discussion on 4-bit vs 8-bit quantization efficiency.",
                "Binary quantization (BQ) is used for fast vector search."
            ]
        },
        {
            "query": "Jina Reranker v2 term proximity",
            "ground_truth": "The reranker provides a proximity bonus when query terms appear close together in the result.",
            "candidates": [
                "Reranking is a process of re-evaluating initial search results.",
                "Jina AI released a new version of their reranker model.",
                "Terms proximity reranker bonus when query together appear close.", # Scrambled
                "The reranker provides a proximity bonus when query terms appear close together in the result.", # Correct
                "Forum post about term proximity in search engines."
            ]
        }
    ]

    # Initialize Ray properly
    ray.init(ignore_reinit_error=True, num_cpus=CPU_CORES_MAX if 'CPU_CORES_MAX' in globals() else 2)

    # Initialize Core Actors to satisfy SearchActor requirements
    workspace = GlobalWorkspace.remote()
    scheduler = Scheduler.remote()

    # Instantiate SearchActor as a remote actor with proper handles
    search_actor = SearchActor.remote(workspace, scheduler)

    total_rr = 0
    print(f"Evaluating {len(test_cases)} test cases...\n")

    for i, case in enumerate(test_cases):
        # Call the rerank method on the remote actor
        ranked = ray.get(search_actor.rerank.remote(case["query"], case["candidates"]))

        rr = calculate_mrr(ranked, case["ground_truth"])
        print(f"[{i+1}] Query: '{case['query']}'")
        print(f"    Top Result: '{ranked[0][:60]}...'")
        print(f"    Reciprocal Rank: {rr:.4f}")
        total_rr += rr

    mrr = total_rr / len(test_cases)
    print(f"\n{'='*50}")
    print(f"Final Mean Reciprocal Rank (MRR): {mrr:.4f}")
    print(f"{'='*50}")

    ray.shutdown()
    return mrr

if __name__ == "__main__":
    # Import config values if available
    try:
        from core.config import CPU_CORES_MAX
    except ImportError:
        CPU_CORES_MAX = 2

    try:
        run_benchmark()
    except Exception as e:
        print(f"Error running benchmark: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
