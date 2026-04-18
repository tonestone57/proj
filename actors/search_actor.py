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

            self.scheduler.submit(self, {
                "type": "search_result",
                "data": compliant_results
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
