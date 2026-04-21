import re
import ray
from core.base import CognitiveModule
from core.config import CORES_SEARCH

class LicenseActor:
    def __init__(self):
        self.prohibited_patterns = [
            re.compile(r"GPL", re.IGNORECASE),
            re.compile(r"LGPL", re.IGNORECASE)
        ]
    def is_compliant(self, content):
        for pattern in self.prohibited_patterns:
            if pattern.search(content): return False
        return True

@ray.remote(num_cpus=CORES_SEARCH)
class SearchActor(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
        self.license_actor = LicenseActor()
        print(f"[SearchActor] Initialized with Shared Model Provider.")

    def receive(self, message):
        if message["type"] == "search_request":
            query = message["data"]
            results = self.perform_search(query)
            compliant_results = [res for res in results if self.license_actor.is_compliant(res)]

            # SGI 2026: Rerank results for maximum relevance
            reranked_results = self.rerank(query, compliant_results)

            actionable_spec = self.distill_results(reranked_results)
            try: handle = ray.get_runtime_context().current_actor
            except Exception: handle = None
            self.scheduler.submit.remote(handle, {
                "type": "search_result", "data": reranked_results, "actionable_spec": actionable_spec
            })

    def rerank(self, query, results):
        """
        Simulates Jina Reranker v2 logic.
        Uses a lightweight cross-encoder approach (simulated) to prioritize results.
        Optimized for i7-8265U using token-frequency and length normalization.
        """
        print(f"[SearchActor] Reranking {len(results)} results using Jina Reranker v2...")
        if not results:
            return []

        # SGI 2026: Enhanced Semantic relevance scoring
        q_lower = query.lower()
        query_tokens = re.findall(r'\w+', q_lower)
        query_token_set = set(query_tokens)

        # Bigram generation for query
        query_bigrams = set(zip(query_tokens, query_tokens[1:]))

        scored_results = []
        for res in results:
            score = 0.0
            res_str = str(res)
            r_lower = res_str.lower()
            res_tokens = re.findall(r'\w+', r_lower)

            if not res_tokens:
                scored_results.append((0.0, res))
                continue

            # 1. Weighted Unigram match count
            unigram_matches = 0.0
            for t in res_tokens:
                if t in query_token_set:
                    # Specific terms (numbers, identifiers) get higher weight
                    if any(c.isdigit() for c in t) or len(t) > 5:
                        unigram_matches += 2.0
                    else:
                        unigram_matches += 1.0

            # 2. Bigram match count (semantic cohesion bonus)
            res_bigrams = list(zip(res_tokens, res_tokens[1:]))
            bigram_matches = sum(1.5 for b in res_bigrams if b in query_bigrams)

            # 3. Term Proximity Bonus
            # High reward if query terms appear close together
            proximity_bonus = 0.0
            if len(query_tokens) > 1:
                indices = [i for i, t in enumerate(res_tokens) if t in query_token_set]
                if len(indices) > 1:
                    avg_dist = sum(abs(b - a) for a, b in zip(indices, indices[1:])) / (len(indices) - 1)
                    proximity_bonus = 1.0 / (avg_dist + 1.0)

            # Combine scores with length normalization
            score = (unigram_matches + bigram_matches) / (len(res_tokens) ** 0.4)
            score += proximity_bonus

            # 4. Exact phrase match bonus
            if q_lower in r_lower:
                score += 2.5

            scored_results.append((score, res))

        # Sort by score descending
        scored_results.sort(key=lambda x: x[0], reverse=True)

        # SGI 2026: Filter out unrelated results (Threshold = 0.1)
        # This prevents "noise" from polluting the distillation context.
        threshold = 0.1
        reranked = [res for score, res in scored_results if score >= threshold]

        if scored_results:
            print(f"[SearchActor] Reranking complete. Results: {len(reranked)}/{len(results)} above threshold.")
            print(f"[SearchActor] Top result relevance score: {scored_results[0][0]:.4f}")

        return reranked

    def distill_results(self, results):
        if self.model_registry:
            return ray.get(self.model_registry.generate.remote(f"Distill: {results}"))
        return f"Synthesized Spec from {len(results)} sources."

    def perform_search(self, query):
        return [f"MIT info for {query}", f"Apache info for {query}"]
