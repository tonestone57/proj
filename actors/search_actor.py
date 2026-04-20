import re
import ray
from core.base import CognitiveModule
from core.config import CORES_SEARCH

@ray.remote
class LicenseActor(CognitiveModule):
    def __init__(self, workspace, scheduler, model_registry=None):
        super().__init__(workspace, scheduler, model_registry)
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
        self.license_actor = LicenseActor.remote(workspace, scheduler, model_registry)
        print(f"[SearchActor] Initialized.")

    def receive(self, message):
        print(f"[SearchActor] Received message: {message}")
        if message["type"] == "search_request":
            query = message["data"]
            results = self.perform_search(query)
            print(f"[SearchActor] Search results: {results}")

            compliant_results = []
            for res in results:
                is_ok = ray.get(self.license_actor.is_compliant.remote(res))
                if is_ok:
                    compliant_results.append(res)

            print(f"[SearchActor] Compliant results: {compliant_results}")
            actionable_spec = self.distill_results(compliant_results)

            try:
                handle = ray.get_runtime_context().current_actor
            except Exception:
                handle = None

            print(f"[SearchActor] Submitting result to scheduler...")
            self.scheduler.submit.remote(handle, {
                "type": "search_result", "data": compliant_results, "actionable_spec": actionable_spec
            })

    def distill_results(self, results):
        if self.model_registry:
            return ray.get(self.model_registry.generate.remote(f"Distill: {results}"))
        return f"Synthesized Spec from {len(results)} sources."

    def perform_search(self, query):
        return [f"MIT info for {query}", f"Apache info for {query}"]
