from core.base import CognitiveModule

class LicenseActor:
    def __init__(self):
        # Keywords that might indicate GPL/LGPL licenses
        self.prohibited_keywords = ["GPL", "LGPL", "General Public License"]

    def is_compliant(self, content):
        """
        Checks if the content is compliant with the No-GPL rule.
        """
        for keyword in self.prohibited_keywords:
            if keyword in content:
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
        # More dynamic mock results
        base_results = [
            {"content": f"Documentation for {query}: Permissive MIT license.", "license": "MIT"},
            {"content": f"Source code for {query}: GPL v3 license included.", "license": "GPL"},
            {"content": f"Technical specification for {query}: Apache 2.0 license.", "license": "Apache"},
        ]

        return [res["content"] for res in base_results]
