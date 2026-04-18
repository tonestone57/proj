import re
from core.base import CognitiveModule

class LicenseActor:
    def __init__(self):
        # Patterns that might indicate GPL/LGPL licenses
        self.prohibited_patterns = [
            re.compile(r"GNU\s+General\s+Public\s+License", re.IGNORECASE),
            re.compile(r"GPLv[123]", re.IGNORECASE),
            re.compile(r"LGPL\s*[0-9\.]*", re.IGNORECASE),
            re.compile(r"Lesser\s+General\s+Public\s+License", re.IGNORECASE),
            re.compile(r"COPYING(?:\.txt|\.md)?", re.IGNORECASE),
            re.compile(r"licensed\s+under\s+the\s+GPL", re.IGNORECASE),
        ]

    def is_compliant(self, content):
        """
        Checks if the content is compliant with the No-GPL rule.
        Uses regex for more robust detection.
        """
        for pattern in self.prohibited_patterns:
            if pattern.search(content):
                return False
        return True

class SearchActor(CognitiveModule):
    def __init__(self, workspace, scheduler):
        super().__init__(workspace, scheduler)
        self.license_actor = LicenseActor()

    def receive(self, message):
        if message["type"] == "search_request":
            query = message["data"]
            results = self.perform_search(query)

            compliant_results = []
            for res in results:
                if self.license_actor.is_compliant(res):
                    compliant_results.append(res)
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
