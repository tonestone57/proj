import re
import ray
import hashlib
import numpy as np
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
    def __init__(self, workspace, scheduler, model_registry=None, graph_memory=None, memory_manager=None):
        super().__init__(workspace, scheduler, model_registry)
        self.license_actor = LicenseActor()
        self.knowledge_graph = graph_memory
        self.memory_manager = memory_manager
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

                current_subgraphs = []
                if potential_nodes:
                    # SGI 2026: Batched Ray remote calls for zero-latency context retrieval
                    futures = [self.knowledge_graph.get_context_subgraph.remote(node) for node in potential_nodes]
                    results_sg = ray.get(futures)

                    for node, sg in zip(potential_nodes, results_sg):
                        if sg["edges"]:
                            current_subgraphs.append(f"Related to {node}: {sg['edges']}")

                if current_subgraphs:
                    graph_context = "\n[Graph Context] " + " | ".join(current_subgraphs)

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
            # SGI 2026: Reasoning-Aware RAG. Retrieve wisdom traces from knowledge base.
            print("[SearchActor] Retrieving Reasoning Traces from Wisdom Cache via MemoryManager...")

            wisdom_traces = []
            if self.memory_manager:
                # Query MemoryManager for relevant traces
                wisdom_traces = ray.get(self.memory_manager.retrieve_wisdom_traces.remote(str(results)))

            wisdom_context = "\n".join([f"[Wisdom Cache] {t}" for t in wisdom_traces]) if wisdom_traces else "[Wisdom Cache] (No relevant traces found)"

            distilled = ray.get(self.model_registry.generate.remote(f"Distill with Context: {wisdom_context}\nData: {results}"))
        else:
            distilled = f"Synthesized Spec from {len(results)} sources."

        # SGI 2026: Add verification warning for forum content
        if has_forum:
            distilled += "\n\n⚠️ [Verification Required] This response includes data from forum posts, which may be less accurate."

        return distilled

    def embed(self, text, dimensions=768):
        """
        Simulates nomic-embed-text-v1.5 embedding generation.
        Returns a mock vector of specified dimensions.
        SGI 2026: Improved mock embedding to utilize all dimensions.
        """
        # Use multiple hashes to fill the vector dimensions
        vector = []
        for i in range((dimensions // 128) + 1):
            seed = f"{text}_{i}"
            hash_val = int(hashlib.md5(seed.encode()).hexdigest(), 16)
            for j in range(128):
                if len(vector) < dimensions:
                    vector.append(((hash_val >> j) & 1) * 2.0 - 1.0) # Scale to [-1, 1]
        return vector

    def binary_quantize(self, vector):
        """
        SGI 2026: Converts a float vector to a packed bit representation (numpy uint64).
        Packs 128 bits into two 64-bit integers.
        """
        bits = [1 if x > 0 else 0 for x in vector]
        # Pack bits into uint64
        packed = []
        for i in range(0, len(bits), 64):
            chunk = bits[i:i+64]
            val = 0
            for j, bit in enumerate(chunk):
                if bit:
                    val |= (1 << j)
            packed.append(np.uint64(val))
        return np.array(packed, dtype=np.uint64)

    def simd_batch_hamming(self, query_packed, candidates_packed_batch):
        """
        SGI 2026: Performs SIMD-based vector shuffling for Matryoshka-tier re-ranking.
        Performs the 128-dim coarse scan across 4 vectors simultaneously using AVX2-style numpy operations.
        candidates_packed_batch shape: (4, 2) - 4 vectors, each with two uint64 elements.
        """
        # Simulated AVX2 256-bit registers (4 x 64-bit uint64)
        # Register 1: bits 0-63 for all 4 candidates
        # Register 2: bits 64-127 for all 4 candidates
        reg1 = candidates_packed_batch[:, 0]
        reg2 = candidates_packed_batch[:, 1]

        # XOR with query bits (broadcast)
        xor1 = np.bitwise_xor(reg1, query_packed[0])
        xor2 = np.bitwise_xor(reg2, query_packed[1])

        # Bitwise count (popcount) of matches
        # Hamming distance is popcount(v1 ^ v2). Similarity is 128 - popcount(v1 ^ v2).
        # However, it's faster to just use bitwise NOT XOR for direct match counting.
        match1 = np.bitwise_count(np.bitwise_not(xor1))
        match2 = np.bitwise_count(np.bitwise_not(xor2))

        return (match1 + match2).astype(int)

    def tiered_search(self, query, top_k_coarse=50, top_k_fine=5):
        """
        SGI 2026: Matryoshka-Tiered Retrieval (Coarse-to-Fine).
        Stage 1: 128-dim scan for speed (SIMD-optimized).
        Stage 2: 768-dim re-rank for accuracy.
        """
        print(f"[SearchActor] Matryoshka-Tiered Retrieval + BQ initiated for: '{query}'")
        query_vec = self.embed(query)
        query_coarse_bq = self.binary_quantize(query_vec[:128])

        # Stage 1: Coarse Scan (SIMD Optimized)
        print(f"[SearchActor] Stage 1: Scanning 128-dim BQ indices (SIMD/AVX2 optimized)...")
        candidates = []
        batch_size = 4
        pool_size = 200

        # Pre-generate or simulate candidate pool
        candidate_data = []
        for i in range(pool_size):
            item_text = f"Knowledge Item {i} for {query}"
            item_vec = self.embed(item_text)
            item_coarse_bq = self.binary_quantize(item_vec[:128])
            candidate_data.append({"text": item_text, "vec": item_vec, "packed": item_coarse_bq})

        # Process in batches of 4 for SIMD simulation
        for i in range(0, pool_size, batch_size):
            batch = candidate_data[i : i + batch_size]
            if len(batch) < batch_size:
                # Handle remainder
                for item in batch:
                    xor1 = np.bitwise_xor(item["packed"][0], query_coarse_bq[0])
                    xor2 = np.bitwise_xor(item["packed"][1], query_coarse_bq[1])
                    matches = 128 - (int(np.bitwise_count(xor1)) + int(np.bitwise_count(xor2)))
                    candidates.append({"text": item["text"], "vec": item["vec"], "score": matches})
                continue

            packed_batch = np.array([item["packed"] for item in batch])
            scores = self.simd_batch_hamming(query_coarse_bq, packed_batch)

            for j, score in enumerate(scores):
                candidates.append({"text": batch[j]["text"], "vec": batch[j]["vec"], "score": score})

        # Sort and take top_k_coarse
        candidates.sort(key=lambda x: x["score"], reverse=True)
        top_candidates = candidates[:top_k_coarse]

        # Stage 2: Fine Re-rank (768-dim)
        print(f"[SearchActor] Stage 2: Re-ranking top {top_k_coarse} candidates using full 768-dim vectors...")
        fine_results = []
        for cand in top_candidates:
            # Full 768-dim cosine similarity (simulated)
            fine_score = sum(a * b for a, b in zip(query_vec, cand["vec"]))
            fine_results.append({"text": cand["text"], "score": fine_score})

        fine_results.sort(key=lambda x: x["score"], reverse=True)
        return [res["text"] for res in fine_results[:top_k_fine]]

    def perform_search(self, query):
        # SGI 2026: Use tiered retrieval
        return self.tiered_search(query)
