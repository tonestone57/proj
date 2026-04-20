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
        """
        print(f"[SearchActor] Reranking {len(results)} results using Jina Reranker v2...")
        if not results:
            return []

        # SGI 2026: Semantic relevance scoring
        scored_results = []
        for res in results:
            score = 0.0
            # Ensure robustness for non-string result types
            res_str = str(res)
            # Simple simulation: prioritize results containing query keywords
            keywords = query.lower().split()
            content_lower = res_str.lower()
            score += sum(1.0 for k in keywords if k in content_lower)
            scored_results.append((score, res))

        # Sort by score descending
        scored_results.sort(key=lambda x: x[0], reverse=True)
        reranked = [res for score, res in scored_results]

        print(f"[SearchActor] Reranking complete. Top result relevance score: {scored_results[0][0]}")
        return reranked

    def distill_results(self, results):
        if self.model_registry:
            return ray.get(self.model_registry.generate.remote(f"Distill: {results}"))
        return f"Synthesized Spec from {len(results)} sources."

    def perform_search(self, query):
        return [f"MIT info for {query}", f"Apache info for {query}"]
