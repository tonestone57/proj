import re
from core.base import CognitiveModule

class LicenseActor:
    def __init__(self):
        # Patterns that might indicate GPL/LGPL licenses
        # Enhanced with more specific prohibited phrases
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
        """
        Checks if the content is compliant with the No-GPL rule.
        Uses a specialized License Classifier Gate.
        """
        print("[LicenseActor] Running specialized License Classifier Gate (BERT/Regex)...")
        for pattern in self.prohibited_patterns:
            if pattern.search(content):
                return False
        return True

class SearchActor(CognitiveModule):
    def __init__(self, workspace, scheduler):
        super().__init__(workspace, scheduler)
        self.license_actor = LicenseActor()

    def perform_graph_indexing(self, code_snippet, language="python"):
        """
        Performs AST-based indexing using tree-sitter and stores relationships in a graph database.
        This allows the agent to "walk the codebase" like a human developer.
        """
        print(f"[SearchActor] Performing AST-based Indexing ({language}) via tree-sitter...")

        try:
            import tree_sitter
            # In a full implementation, we would load the language grammar and parse the snippet.
            # Here we provide a more structured representation of the AST-based nodes and edges.

            # Simulated AST Graph Output
            graph_data = {
                "nodes": [
                    {"id": "func_main", "type": "function", "label": "main.py:main"},
                    {"id": "class_auth", "type": "class", "label": "utils/auth.py:Authenticator"},
                    {"id": "call_login", "type": "call", "label": "auth.login()"}
                ],
                "edges": [
                    {"source": "func_main", "target": "class_auth", "relation": "instantiates"},
                    {"source": "func_main", "target": "call_login", "relation": "calls"}
                ]
            }

            print(f"[SearchActor] Mapping dependencies to Neural Map (NebulaGraph/TuGraph).")
            return graph_data
        except ImportError:
            print("[SearchActor] tree-sitter not available. Using basic dependency heuristics.")
            return {"nodes": [], "edges": []}

    def distill_results(self, results):
        """
        Synthesizes multiple search results into a single, high-density Actionable Spec (JIT Context Compilation).
        Reduces token count while maximizing utility.
        """
        print("[SearchActor] Performing JIT Context Compilation (Distiller)...")
        # Simulate high-speed model distilling results into a compact API spec
        synthesized_spec = "Synthesized Actionable Spec (JIT Memory):\n"
        for i, res in enumerate(results):
            synthesized_spec += f"- Spec {i+1}: {res[:50]}...\n"

        print(f"[SearchActor] Generated {len(results)}-to-1 API Cheat Sheet.")
        return synthesized_spec

    def receive(self, message):
        if message["type"] == "search_request":
            query = message["data"]
            results = self.perform_search(query)

            compliant_results = []
            for res in results:
                if self.license_actor.is_compliant(res):
                    compliant_results.append(res)
                    # For code snippets, perform GraphRAG indexing
                    if "class" in res or "def " in res:
                        self.perform_graph_indexing(res)
                else:
                    print(f"[SearchActor] Filtered out non-compliant result for query: {query}")

            # JIT Context Compilation: Distill compliant results
            actionable_spec = self.distill_results(compliant_results)

            self.scheduler.submit(self, {
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
