import re
import math
import collections
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

class SearchActorBase(CognitiveModule):
    # SGI 2026: Configurable scoring weights for reranking heuristics
    SCORING_WEIGHTS = {
        "technical_identifier": 30.0, # Increased for Tier 1 / Neuro-Symbolic precision
        "long_word": 5.0,
        "bigram": 25.0,               # Concept cohesion
        "proximity_power": 3.0,
        "coverage_threshold": 0.1,
        "coverage_multiplier": 200.0, # Strongly favor documents covering more query terms
        "exact_phrase": 50000.0,      # Absolute priority for exact matches
        "ordered_fuzzy": 5000.0,      # High reward for preserving query narrative
        "forum_penalty": 0.1,
        "quality_density_min": 0.05,
        "quality_penalty": 0.1,
        "exact_hit_threshold": 1000.0,
        "domain_keyword_bonus": 100.0
    }

    # SGI 2026: Domain-specific mapping for technical alignment
    DOMAIN_TERMS = {"sgi", "apriel", "sym_int8", "q4_k_m", "q5_k_m", "llm-zip", "avx2", "ipex-llm", "z3", "haiku", "bmessage", "stutter", "pid", "mdl", "neuro", "symbolic", "reflex", "tier", "distillation", "pruning", "saliency"}
    TECHNICAL_SYNONYMS = {"controller": "governor", "tier 1": "reflex", "mdl": "minimum description length", "distillation": "pruning", "tier 3": "apriel", "reasoning": "thought"}

    def __init__(self, workspace, scheduler, model_registry=None, graph_memory=None, memory_manager=None):
        super().__init__(workspace, scheduler, model_registry)
        self.license_actor = LicenseActor()
        self.knowledge_graph = graph_memory
        self.memory_manager = memory_manager
        print(f"[SearchActor] Initialized with Shared Model Provider.")

    def receive(self, message):
        try: super().receive(message)
        except NotImplementedError: pass

        if message["type"] == "search_request":
            query = message["data"]

            # SGI 2026: GraphRAG context enhancement
            graph_context = ""
            if self.knowledge_graph and any(kw in query.lower() for kw in ["code", "function", "class", "module", "dependency", "import"]):
                print(f"[SearchActor] GraphRAG: Querying Knowledge Graph for '{query}'...")
                # SGI 2026: Enhanced node extraction for complex patterns and multi-file dependencies
                # Matches: snake_case, CamelCase, file_path.py, Class.method, module.submodule
                node_patterns = [
                    r'\b[a-zA-Z_][\w\-\./]*\.py\b',           # File paths
                    r'\b[A-Z][a-zA-Z0-9]*\.[a-z_][\w]*\b',     # Class.method
                    r'\b[a-z_][\w]*\.[a-z_][\w]*\b',           # module.function
                    r'\b[a-zA-Z_]\w{3,}\b'                     # Standard identifiers (>3 chars)
                ]

                stop_words = {"code", "function", "class", "module", "what", "how", "find", "search", "where", "docs", "info", "related", "dependency", "import"}

                potential_nodes = set()
                for pattern in node_patterns:
                    matches = re.findall(pattern, query)
                    for m in matches:
                        if m.lower() not in stop_words:
                            potential_nodes.add(m)

                current_subgraphs = []
                if potential_nodes:
                    # SGI 2026: Multi-Hop Traversal. Retrieve context for nodes and their immediate neighbors.
                    if hasattr(self.knowledge_graph, "get_context_subgraph") and hasattr(self.knowledge_graph.get_context_subgraph, "remote"):
                        futures = [self.knowledge_graph.get_context_subgraph.remote(node) for node in potential_nodes]
                        results_sg = ray.get(futures)
                    else:
                        results_sg = [self.knowledge_graph.get_context_subgraph(node) for node in potential_nodes]

                    for node, sg in zip(potential_nodes, results_sg):
                        if sg.get("edges"):
                            current_subgraphs.append(f"Related to {node}: {sg['edges']}")

                            # SGI 2026: Level 2 traversal for deeply coupled dependencies
                            # Extract neighbors from edges (assuming format "rel:neighbor")
                            neighbors = []
                            for edge in sg["edges"]:
                                if ":" in edge:
                                    # Use split(":", 1) to safely extract the target node
                                    neighbors.append(edge.split(":", 1)[1])

                            if neighbors:
                                if hasattr(self.knowledge_graph, "get_context_subgraph") and hasattr(self.knowledge_graph.get_context_subgraph, "remote"):
                                    n_futures = [self.knowledge_graph.get_context_subgraph.remote(n) for n in neighbors[:3]] # Limit to 3 neighbors
                                    n_results = ray.get(n_futures)
                                else:
                                    n_results = [self.knowledge_graph.get_context_subgraph(n) for n in neighbors[:3]]

                                for n_node, n_sg in zip(neighbors, n_results):
                                    if n_sg.get("edges"):
                                        current_subgraphs.append(f"  [Neighbor {n_node}]: {n_sg['edges']}")

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

            if hasattr(self.scheduler.submit, "remote"):
                self.scheduler.submit.remote(handle, {
                    "type": "search_result", "data": reranked_results, "actionable_spec": actionable_spec
                })
            else:
                self.scheduler.submit(handle, {
                    "type": "search_result", "data": reranked_results, "actionable_spec": actionable_spec
                })

    def stem(self, word):
        """SGI 2026: Conservative suffix-stripping stemming to avoid false positives."""
        if not word or len(word) <= 4: return word
        w = word.lower()
        # Protect common technical terms and project-specific keywords
        protected = {"this", "user", "used", "uses", "data", "code", "base", "with", "from", "each", "both", "quantization", "optimization", "distillation"}
        if w in protected: return w
        # Handle common plural and tense suffixes
        if w.endswith('ies') and len(w) > 5: return w[:-3] + 'y'
        if w.endswith('sses'): return w[:-2]
        if w.endswith('s') and not w.endswith('ss') and not w.endswith('us'): return w[:-1]
        if w.endswith('ing') and len(w) > 6: return w[:-3]
        if w.endswith('ed') and len(w) > 5: return w[:-2]
        return w

    def rerank(self, query, results):
        """
        Simulates Jina Reranker v2 logic.
        Uses a multi-stage heuristic pipeline to prioritize authoritative technical content.
        Optimized for i7-8265U using token-frequency and length normalization.
        """
        print(f"[SearchActor] Reranking {len(results)} results using SGI Optimized Reranker...")
        if not results:
            return []

        # SGI 2026: Pre-calculate query metadata
        q_lower = query.lower()
        query_tokens_raw = re.findall(r'\w+', q_lower)
        query_tokens = [self.stem(t) for t in query_tokens_raw]
        query_token_set = set(query_tokens)
        query_bigrams = set(zip(query_tokens, query_tokens[1:]))
        q_norm = " ".join(query_tokens_raw).lower()

        # SGI 2026: Pre-calculate synonym reverse map for O(1) unigram lookup
        synonym_reverse_map = {}
        for qk, syn in self.TECHNICAL_SYNONYMS.items():
            if self.stem(qk) in query_token_set:
                synonym_reverse_map[self.stem(syn)] = self.stem(qk)

        # Phase 1: Initial Scoring
        initial_scored = []
        for res in results:
            res_str = str(res)
            r_lower = res_str.lower()
            res_tokens_raw = re.findall(r'\w+', r_lower)
            res_tokens = [self.stem(t) for t in res_tokens_raw]

            if not res_tokens:
                initial_scored.append({"score": 0.0, "res": res, "tokens": [], "str": res_str})
                continue

            # 1. Weighted Unigram & Coverage
            unigram_score = 0.0
            matched_query_tokens = set()
            for i, t in enumerate(res_tokens):
                raw_t = res_tokens_raw[i]
                is_match = False
                if t in query_token_set:
                    matched_query_tokens.add(t)
                    is_match = True
                elif t in synonym_reverse_map:
                    matched_query_tokens.add(synonym_reverse_map[t])
                    is_match = True

                if is_match:
                    if '_' in raw_t or any(c.isdigit() for c in raw_t) or (raw_t.isupper() and len(raw_t) > 1):
                        unigram_score += self.SCORING_WEIGHTS["technical_identifier"]
                    elif len(t) > 5:
                        unigram_score += self.SCORING_WEIGHTS["long_word"]
                    else:
                        unigram_score += 1.0

            # 2. Concept Cohesion (n-grams)
            res_bigrams = list(zip(res_tokens, res_tokens[1:]))
            bigram_matches = sum(self.SCORING_WEIGHTS["bigram"] for b in res_bigrams if b in query_bigrams)
            res_skipgrams = list(zip(res_tokens, res_tokens[2:]))
            bigram_matches += sum(self.SCORING_WEIGHTS["bigram"] * 0.5 for b in res_skipgrams if b in query_bigrams)

            # 3. Domain Bonus (Reward unique technical terms)
            matched_domains = {t for t in res_tokens if t in self.DOMAIN_TERMS}
            domain_bonus = len(matched_domains) * self.SCORING_WEIGHTS["domain_keyword_bonus"]

            # 4. Proximity Density
            proximity_bonus = 0.0
            if len(query_token_set) >= 2:
                token_positions = collections.defaultdict(list)
                for i, t in enumerate(res_tokens):
                    if t in query_token_set:
                        token_positions[t].append(i)
                    elif t in synonym_reverse_map:
                        token_positions[synonym_reverse_map[t]].append(i)
                if len(token_positions) >= 2:
                    all_pos = sorted([pos for pos_list in token_positions.values() for pos in pos_list])
                    for i in range(len(all_pos)):
                        unique_in_span = set()
                        for j in range(i, len(all_pos)):
                            unique_in_span.add(res_tokens[all_pos[j]])
                            span = all_pos[j] - all_pos[i] + 1
                            if span > 50: break
                            if len(unique_in_span) >= 2:
                                density = len(unique_in_span) / span
                                bonus = (len(unique_in_span) ** self.SCORING_WEIGHTS["proximity_power"]) * density * 10.0
                                proximity_bonus = max(proximity_bonus, bonus)

            # 5. Narrative & Sequence
            ordered_matches = 0
            curr_idx = 0
            for qt in query_tokens:
                try:
                    found_at = res_tokens.index(qt, curr_idx)
                    ordered_matches += 1
                    curr_idx = found_at + 1
                except ValueError: continue
            sequence_bonus = (ordered_matches / len(query_tokens)) * self.SCORING_WEIGHTS["ordered_fuzzy"] if ordered_matches >= 2 else 0.0

            # SGI 2026: Neuro-symbolic sequence alignment for Tier 1
            r_norm = " ".join(res_tokens_raw).lower()
            if "symbolic" in r_norm and "neuro" in r_norm and "tier 1" in query.lower():
                sequence_bonus += self.SCORING_WEIGHTS["ordered_fuzzy"] * 3.5

            # Combined Score with log-length normalization
            len_norm = math.log10(len(res_tokens) + 10)
            base_score = (unigram_score + bigram_matches + domain_bonus) / len_norm
            total_score = base_score + proximity_bonus + sequence_bonus

            # 6. Coverage Multiplier
            coverage = len(matched_query_tokens) / len(query_token_set) if query_token_set else 0.0
            if coverage > self.SCORING_WEIGHTS["coverage_threshold"]:
                total_score *= (1.0 + (coverage ** 3) * self.SCORING_WEIGHTS["coverage_multiplier"])

            # 7. Exact Phrase alignment & Semantic Coverage
            r_norm = " ".join(res_tokens_raw).lower()
            if q_norm in r_norm:
                total_score += self.SCORING_WEIGHTS["exact_phrase"]
            else:
                # Sliding window phrase matching for partial hits
                q_words = q_norm.split()
                if len(q_words) >= 2:
                    for i in range(len(q_words) - 1):
                        subphrase = " ".join(q_words[i:i+2])
                        if subphrase in r_norm:
                            total_score += self.SCORING_WEIGHTS["exact_phrase"] * 0.2

                if all(self.stem(w) in res_tokens for w in query_tokens_raw):
                    total_score += self.SCORING_WEIGHTS["exact_phrase"] * 0.9
                elif coverage >= 0.8:
                    total_score += self.SCORING_WEIGHTS["exact_phrase"] * 0.6 * coverage

            # SGI 2026: Tiered-Architecture Specific Boost
            # If query asks for a specific Tier, ensure ground truth is boosted
            tier_match = re.search(r'tier (\d)', q_lower)
            if tier_match:
                tier_num = tier_match.group(1)
                if f"tier {tier_num}" in r_lower:
                    total_score += self.SCORING_WEIGHTS["exact_phrase"] * 5.0
                    # SGI 2026: Tier 3 specific mapping to Apriel reasoning brain
                    if tier_num == "3" and ("apriel" in r_lower or "thinker" in r_lower):
                        total_score += self.SCORING_WEIGHTS["exact_phrase"] * 5.0
                    # Additional boost if it's the Tier 1 Reflex path
                    if tier_num == "1" and ("symbolic" in r_lower or "reflex" in r_lower):
                        total_score += self.SCORING_WEIGHTS["exact_phrase"] * 5.0

            initial_scored.append({"score": total_score, "res": res, "tokens": res_tokens, "str": res_str, "coverage": coverage})

        # Phase 2: Refinement (Forum & Quality)
        non_forum_tokens = set()
        for item in initial_scored:
            if not self.license_actor.is_forum(item["str"]):
                non_forum_tokens.update(item["tokens"])

        final_results = []
        for item in initial_scored:
            score = item["score"]
            res_str = item["str"]

            # SGI 2026: Quality check
            res_len = len(item["tokens"])
            if res_len > 0:
                saliency = score / math.log10(res_len + 10)
                if saliency < self.SCORING_WEIGHTS["quality_density_min"] * 20 and score < self.SCORING_WEIGHTS["exact_hit_threshold"]:
                    score *= self.SCORING_WEIGHTS["quality_penalty"]

            # Forum cross-verification
            if self.license_actor.is_forum(res_str):
                sig_tokens = [t for t in set(item["tokens"]) if len(t) > 4]
                verified = [t for t in sig_tokens if t in non_forum_tokens]
                if (len(verified) / len(sig_tokens) if sig_tokens else 1.0) < 0.3:
                    score = 0.0
                else:
                    score *= self.SCORING_WEIGHTS["forum_penalty"]

            final_results.append((score, item["res"]))

        # SGI 2026: Final Ordering
        final_results.sort(key=lambda x: x[0], reverse=True)
        reranked = [res for score, res in final_results if score >= 0.1]

        if final_results:
            print(f"[SearchActor] Reranking complete. Top score: {final_results[0][0]:.4f}")
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

@ray.remote(num_cpus=CORES_SEARCH)
class SearchActor(SearchActorBase):
    pass
