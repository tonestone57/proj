import re
import ray
import asyncio
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
        print(f"[SearchActor] Initialized with Shared Model Provider.")

    async def receive(self, message):
        print(f"[SearchActor] Received message: {message['type']}")
        if message["type"] == "search_request":
            query = message["data"]
            results = self.perform_search(query)

            # Async gather to avoid blocking
            compliance_results = await asyncio.gather(*[self.license_actor.is_compliant.remote(res) for res in results])
            compliant_results = [res for res, is_ok in zip(results, compliance_results) if is_ok]

            actionable_spec = await self.distill_results_async(compliant_results)

            try: handle = ray.get_runtime_context().current_actor
            except Exception: handle = None

            self.scheduler.submit.remote(handle, {
                "type": "search_result", "data": compliant_results, "actionable_spec": actionable_spec
            })

    async def distill_results_async(self, results):
        if self.model_registry:
            return await self.model_registry.generate.remote(f"Distill: {results}")
        return f"Synthesized Spec from {len(results)} sources."

    def perform_search(self, query):
        return [f"MIT info for {query}", f"Apache info for {query}"]
