"""
SGI-Alpha Search Accuracy Benchmark
-----------------------------------
This tool implements the internal accuracy benchmark for the SGI architecture,
focusing on the Search Reranker accuracy using Mean Reciprocal Rank (MRR).

It evaluates the SearchActor's ability to prioritize authoritative technical
content over forum posts and noise, as defined in the SGI-2026 roadmap.
"""

import sys
import os
import ray
import re

# Standard SGI imports and environment setup
sys.path.append(os.getcwd())

try:
    from core.config import CPU_CORES_MAX
except ImportError:
    CPU_CORES_MAX = 2

from core.workspace import GlobalWorkspace
from core.scheduler import Scheduler
from actors.search_actor import SearchActor

# Benchmark Data: Diverse ground truth test cases
TEST_CASES = [
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
            "Terms proximity reranker bonus when query together appear cl...",
            "The reranker provides a proximity bonus when query terms appear close together in the result.",
            "Forum post about term proximity in search engines."
        ]
    },
    {
        "query": "Minimum Description Length principle",
        "ground_truth": "According to the Minimum Description Length (MDL) principle, the best understanding of a dataset is the shortest program that can recreate it.",
        "candidates": [
            "MDL is a concept used in statistical modeling and machine learning.",
            "According to the Minimum Description Length (MDL) principle, the best understanding of a dataset is the shortest program that can recreate it.",
            "Shortest programs are usually better for compression.",
            "Forum: What is MDL in the context of SGI?",
            "Information theory and its relationship to cognitive density."
        ]
    },
    {
        "query": "Ray distributed orchestrator configuration",
        "ground_truth": "Ray is used as the primary distributed orchestrator to manage resources (configured for 1-2 CPU cores per actor).",
        "candidates": [
            "Ray is a popular framework for scaling Python applications.",
            "Docker and Kubernetes are also used for orchestration.",
            "Ray is used as the primary distributed orchestrator to manage resources (configured for 1-2 CPU cores per actor).",
            "Forum: Help with Ray resource allocation.",
            "Setting up a local Ray instance for testing."
        ]
    },
    {
        "query": "Haiku OS BMessage syntax",
        "ground_truth": "Haiku OS utilizes BMessage for flexible, flattenable data containers in inter-app communication.",
        "candidates": [
            "Haiku is an open-source operating system that targets personal computing.",
            "BMessage is used for messaging in BeOS and Haiku.",
            "Haiku OS utilizes BMessage for flexible, flattenable data containers in inter-app communication.",
            "Forum: Coding for Haiku is fun.",
            "Differences between Haiku and Linux system calls."
        ]
    },
    {
        "query": "Z3 SMT Solver verification",
        "ground_truth": "Integration with Z3 SMT Solver ensures code correctness by proving the absence of undefined states.",
        "candidates": [
            "Z3 is a theorem prover from Microsoft Research.",
            "SMT solvers are used for various software engineering tasks.",
            "Integration with Z3 SMT Solver ensures code correctness by proving the absence of undefined states.",
            "Forum: How to install Z3-solver on Python.",
            "Using formal methods to verify distributed systems."
        ]
    },
    {
        "query": "PID Controller thermal management",
        "ground_truth": "The PID governor maintains CPU temperature by calculating a stutter interval based on thermal error.",
        "candidates": [
            "PID controllers are common in industrial control systems.",
            "The PID governor maintains CPU temperature by calculating a stutter interval based on thermal error.",
            "Micro-stuttering is an effective way to cool down mobile CPUs.",
            "Forum: My i7 is running too hot.",
            "Implementing Proportional-Integral-Derivative logic in Python."
        ]
    },
    {
        "query": "Neuro-Symbolic architecture Tier 1",
        "ground_truth": "Tier 1 Reflex path utilizes Symbolic logic (Python/Regex/Z3) for instant, low-cost responses.",
        "candidates": [
            "Neuro-symbolic AI combines neural networks and symbolic reasoning.",
            "Tier 1 Reflex path utilizes Symbolic logic (Python/Regex/Z3) for instant, low-cost responses.",
            "SGI architecture has 4 tiers of cognitive processing.",
            "Forum: What's the difference between Tier 1 and Tier 3?",
            "Fast path vs slow path in cognitive architectures."
        ]
    },
    {
        "query": "MemoryManager synaptic pruning",
        "ground_truth": "MemoryManager performs synaptic pruning to evict low-saliency memories based on information density.",
        "candidates": [
            "Synaptic pruning is a biological process in the brain.",
            "MemoryManager performs synaptic pruning to evict low-saliency memories based on information density.",
            "Information density is measured using Shannon entropy.",
            "Forum: How does SGI manage its RAM?",
            "Archiving logs to LanceDB using Zstd-19."
        ]
    },
    {
        "query": "SGI thermal governor",
        "ground_truth": "The PID governor maintains CPU temperature by calculating a stutter interval based on thermal error.",
        "candidates": [
            "The system uses a basic thermal controller.",
            "The PID governor maintains CPU temperature by calculating a stutter interval based on thermal error.",
            "Forum: How do I control my CPU temp?",
            "Technical details on PID loop frequency.",
            "Governor vs controller: a nomenclature debate."
        ]
    },
    {
        "query": "Apriel reasoning trace distillation",
        "ground_truth": "Apriel utilizes the MemoryManager to perform reasoning trace distillation (synaptic pruning) on low-saliency memories.",
        "candidates": [
            "Apriel model uses standard RAG for retrieval.",
            "Reasoning traces are stored in the Wisdom Cache.",
            "Apriel utilizes the MemoryManager to perform reasoning trace distillation (synaptic pruning) on low-saliency memories.",
            "Distillation is a process of knowledge transfer.",
            "Forum: What is Apriel distillation?"
        ]
    },
    {
        "query": "Tier 3 Reasoning Path",
        "ground_truth": "Tier 3 Reasoning Path: Higher-order reasoning (Planning, Complex Coding) via Apriel-1.6-15B-Thinker.",
        "candidates": [
            "Tier 1 handles reflex tasks.",
            "Tier 3 utilizes the 0.8B model for speed.",
            "Tier 3 Reasoning Path: Higher-order reasoning (Planning, Complex Coding) via Apriel-1.6-15B-Thinker.",
            "Memory retrieval is a Tier 2 process.",
            "Forum: Help with Tier 3 configuration."
        ]
    }
]

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
    """
    Executes the SGI Search Accuracy Benchmark.
    """
    print("--- SGI-Alpha Search Accuracy Benchmark (Reranker MRR) ---")

    # Initialize Ray properly for the SGI environment
    ray.init(ignore_reinit_error=True, num_cpus=CPU_CORES_MAX)

    try:
        # Initialize Core Actors to satisfy SearchActor requirements
        workspace = GlobalWorkspace.remote()
        scheduler = Scheduler.remote()

        # Instantiate SearchActor as a remote actor with proper handles
        search_actor = SearchActor.remote(workspace, scheduler)

        total_rr = 0
        print(f"Evaluating {len(TEST_CASES)} test cases...\n")

        for i, case in enumerate(TEST_CASES):
            # Call the rerank method on the remote actor
            ranked = ray.get(search_actor.rerank.remote(case["query"], case["candidates"]))

            rr = calculate_mrr(ranked, case["ground_truth"])
            print(f"[{i+1}] Query: '{case['query']}'")
            print(f"    Top Result: '{ranked[0][:60]}...'")
            print(f"    Reciprocal Rank: {rr:.4f}")
            total_rr += rr

    except Exception:
        import traceback
        traceback.print_exc()
        return 0.0
    finally:
        mrr = total_rr / len(TEST_CASES) if TEST_CASES else 0.0
        print(f"\n{'='*50}")
        print(f"Final Mean Reciprocal Rank (MRR): {mrr:.4f}")
        print(f"{'='*50}")
        ray.shutdown()

    return mrr

if __name__ == "__main__":
    try:
        run_benchmark()
    except Exception as e:
        print(f"Error running benchmark: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
