import re
import ray
from core.base import CognitiveModule
from ipex_llm.transformers import AutoModelForCausalLM
from core.config import CORES_SEARCH

class LicenseActor:
    def __init__(self):
        self.prohibited_patterns = [
            re.compile(r"GNU\s+General\s+Public\s+License", re.IGNORECASE),
            re.compile(r"GPLv[123]", re.IGNORECASE),
            re.compile(r"LGPL\s*[0-9\.]*", re.IGNORECASE),
            re.compile(r"Lesser\s+General\s+Public\s+License", re.IGNORECASE),
            re.compile(r"COPYING(?:\.txt|\.md)?", re.IGNORECASE),
            re.compile(r"licensed\s+under\s+the\s+GPL", re.IGNORECASE),
            re.compile(r"Free\s+Software\s+Foundation", re.IGNORECASE),
            re.compile(r"vulnerability\s+to\s+viral\s+licensing", re.IGNORECASE),
            re.compile(r"Affero\s+General\s+Public\s+License", re.IGNORECASE),
            re.compile(r"AGPLv[123]", re.IGNORECASE),
            re.compile(r"license\s+is\s+viral", re.IGNORECASE),
            re.compile(r"strictly\s+prohibited\s+without\s+FSF\s+approval", re.IGNORECASE),
        ]

    def is_compliant(self, content):
        for pattern in self.prohibited_patterns:
            if pattern.search(content): return False
        return True

@ray.remote(num_cpus=CORES_SEARCH)
class SearchActor(CognitiveModule):
    def __init__(self, workspace, scheduler, model_id="intel/neural-chat-14b-v3-3"):
        super().__init__(workspace, scheduler)
        self.license_actor = LicenseActor()
        print(f"[SearchActor] Loading {model_id} in NF4 precision for search distillation...")
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                load_in_low_bit="nf4",
                trust_remote_code=True,
                use_cache=True
            )
        except Exception as e:
            print(f"[SearchActor] Error loading model: {e}. Using mock model.")
            self.model = None

    def perform_graph_indexing(self, code_snippet, language="python"):
        print(f"[SearchActor] Performing AST-based Indexing ({language}) via tree-sitter...")
        try:
            import tree_sitter
            # Simulating AST Graph Output as requested in AGENTS.md
            return {
                "nodes": [
                    {"id": "func_main", "type": "function", "label": "main.py:main"},
                    {"id": "class_auth", "type": "class", "label": "utils/auth.py:Authenticator"}
                ],
                "edges": [{"source": "func_main", "target": "class_auth", "relation": "instantiates"}]
            }
        except ImportError:
            return {"nodes": [{"id": "snippet", "type": "code", "label": "Search Result"}], "edges": []}

    def distill_results(self, results):
        print("[SearchActor] Performing JIT Context Compilation (Distiller)...")
        synthesized_spec = "Synthesized Actionable Spec (JIT Memory):\n"
        for i, res in enumerate(results): synthesized_spec += f"- Spec {i+1}: {res[:50]}...\n"
        return synthesized_spec

    def receive(self, message):
        if message["type"] == "search_request":
            query = message["data"]
            results = self.perform_search(query)
            compliant_results = []
            for res in results:
                if self.license_actor.is_compliant(res):
                    compliant_results.append(res)
                    if "class" in res or "def " in res: self.perform_graph_indexing(res)
            actionable_spec = self.distill_results(compliant_results)
            self.scheduler.submit.remote(ray.get_runtime_context().get_actor_handle(), {
                "type": "search_result",
                "data": compliant_results,
                "actionable_spec": actionable_spec
            })

    def perform_search(self, query):
        """
        Simulates an autonomous online search.
        In a real scenario, this would call Tavily or SearXNG.
        """
        # Dynamic mock results based on query
        return [
            f"Documentation for {query}: Permissive MIT license summary.",
            f"Technical spec for {query}: Licensed under Apache 2.0.",
            f"Implementation details for {query}: See GPLv3 source for more info.",
            f"Quick start guide for {query}: Included in COPYING file."
        ]

    def MultiPerspectiveSearch(self, query):
        """
        Employs Multi-Perspective Search—querying both the main thesis and its antithesis.
        """
        print(f"[SearchActor] Performing Multi-Perspective Search for: {query}")
        queries = [
            query,
            f"limitations of {query}",
            f"alternatives to {query}",
            f"why {query} might fail"
        ]

        all_results = []
        for q in queries:
            all_results.extend(self.perform_search(q))
        return all_results

    def NebulaGraph_Emitter(self, graph_data):
        """
        Simulates AST-based node/edge persistence in NebulaGraph.
        """
        print("[SearchActor] Emitting graph data to NebulaGraph (The Neural Map)...")
        for node in graph_data.get("nodes", []):
            print(f"  INSERT VERTEX (ID: {node['id']}, TYPE: {node['type']})")
        for edge in graph_data.get("edges", []):
            print(f"  INSERT EDGE (FROM: {edge['source']}, TO: {edge['target']}, REL: {edge['relation']})")
        return True

    def calculate_retrieval_confidence(self, query, results):
        """
        Scores retrieval confidence based on result relevance to the query.
        """
        if not results:
            return 0.0

        relevance_score = 0
        query_terms = set(query.lower().split())
        for res in results:
            res_terms = set(res.lower().split())
            if query_terms.intersection(res_terms):
                relevance_score += 1

        confidence = relevance_score / len(results)
        return min(1.0, confidence)
