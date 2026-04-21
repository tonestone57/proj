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
        # SGI 2026: Forum detection patterns for accuracy safeguarding
        self.forum_patterns = [
            re.compile(r"reddit\.com", re.IGNORECASE),
            re.compile(r"stackoverflow\.com", re.IGNORECASE),
            re.compile(r"discourse", re.IGNORECASE),
            re.compile(r"forum", re.IGNORECASE)
        ]

    def is_compliant(self, content):
        for pattern in self.prohibited_patterns:
            if pattern.search(content): return False
        return True

    def is_forum(self, content):
        for pattern in self.forum_patterns:
            if pattern.search(content): return True
        return False

@ray.remote(num_cpus=CORES_SEARCH)
class SearchActor(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None, graph_memory=None):
        super().__init__(workspace, scheduler, model_registry)
        self.license_actor = LicenseActor()
        self.knowledge_graph = graph_memory
        print(f"[SearchActor] Initialized with Shared Model Provider.")

    def receive(self, message):
        if message["type"] == "search_request":
            query = message["data"]

            # SGI 2026: GraphRAG context enhancement
            graph_context = ""
            if self.knowledge_graph and ("code" in query or "function" in query):
                print(f"[SearchActor] GraphRAG: Querying Knowledge Graph for '{query}'...")
                # Extract potential node name from query, filtering out common terms
                stop_words = {"code", "function", "what", "how", "find", "search", "where", "docs", "info", "related"}
                # SGI 2026: Refined node extraction regex to prioritize snake_case or CamelCase identifiers
                potential_nodes = [n for n in re.findall(r'\b[a-zA-Z_]\w*\b', query) if len(n) > 3 and n.lower() not in stop_words]

                subgraphs = []
                if potential_nodes:
                    # SGI 2026: Batched Ray remote calls for zero-latency context retrieval
                    futures = [self.knowledge_graph.get_context_subgraph.remote(node) for node in potential_nodes]
                    results_sg = ray.get(futures)

                    for node, sg in zip(potential_nodes, results_sg):
                        if sg["edges"]:
                            subgraphs.append(f"Related to {node}: {sg['edges']}")

                if subgraphs:
                    graph_context = "\n[Graph Context] " + " | ".join(subgraphs)

            results = self.perform_search(query)
            compliant_results = [res for res in results if self.license_actor.is_compliant(res)]

            # SGI 2026: Rerank results for maximum relevance
            reranked_results = self.rerank(query, compliant_results)

            actionable_spec = self.distill_results(reranked_results)
            if graph_context:
                actionable_spec = graph_context + "\n" + actionable_spec

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

            # SGI 2026: Forum Accuracy Penalty
            # Forum posts are prioritized lower due to potential inaccuracies.
            if self.license_actor.is_forum(res_str):
                score *= 0.5

            scored_results.append((score, res))

        # SGI 2026: Forum Cross-Verification Logic
        # If a result is a forum post, verify its content against non-forum results.
        final_scored_results = []
        non_forum_text = " ".join([str(res).lower() for score, res in scored_results if not self.license_actor.is_forum(str(res))])

        for score, res in scored_results:
            res_str = str(res)
            if self.license_actor.is_forum(res_str):
                # Check if forum keywords exist in more authoritative content
                res_tokens = set(re.findall(r'\w+', res_str.lower()))
                # Ignore common words
                significant_tokens = [t for t in res_tokens if len(t) > 4]
                verified_tokens = [t for t in significant_tokens if t in non_forum_text]

                verification_ratio = len(verified_tokens) / len(significant_tokens) if significant_tokens else 1.0

                if verification_ratio < 0.3:
                    # Unverified forum post: Exclude by setting score to 0
                    score = 0.0
                else:
                    # Verified forum post: Keep but maintain penalty
                    pass

            final_scored_results.append((score, res))

        # Sort by score descending
        final_scored_results.sort(key=lambda x: x[0], reverse=True)

        # SGI 2026: Filter out unrelated results (Threshold = 0.1)
        # This prevents "noise" from polluting the distillation context.
        threshold = 0.1
        reranked = [res for score, res in final_scored_results if score >= threshold]

        if final_scored_results:
            print(f"[SearchActor] Reranking complete. Results: {len(reranked)}/{len(results)} above threshold.")
            print(f"[SearchActor] Top result relevance score: {final_scored_results[0][0]:.4f}")

        return reranked

    def distill_results(self, results):
        has_forum = any(self.license_actor.is_forum(str(r)) for r in results)

        distilled = ""
        if self.model_registry:
            distilled = ray.get(self.model_registry.generate.remote(f"Distill: {results}"))
        else:
            distilled = f"Synthesized Spec from {len(results)} sources."

        # SGI 2026: Add verification warning for forum content
        if has_forum:
            distilled += "\n\n⚠️ [Verification Required] This response includes data from forum posts, which may be less accurate."

        return distilled

    def perform_search(self, query):
        return [f"MIT info for {query}", f"Apache info for {query}"]
