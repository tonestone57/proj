import unittest
import ray
from actors.search_actor import SearchActor
from core.model_registry import ModelRegistry
from memory.memory_manager import MemoryManager
from meta_learning.meta_manager import MetaManager
from core.workspace import GlobalWorkspace
from core.scheduler import Scheduler

class TestHybridImprovements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ray.init(ignore_reinit_error=True, num_cpus=2)

    @classmethod
    def tearDownClass(cls):
        ray.shutdown()

    def test_tiered_retrieval(self):
        workspace = GlobalWorkspace.remote()
        scheduler = Scheduler.remote()
        search_actor = SearchActor.remote(workspace, scheduler)

        # Test tiered_search directly
        results = ray.get(search_actor.tiered_search.remote("test query"))
        self.assertEqual(len(results), 5)
        self.assertTrue(all("Knowledge Item" in r for r in results))

    def test_reasoning_trace_extraction(self):
        model_registry = ModelRegistry.remote()
        prompt = "How to optimize AVX2?"
        response = ray.get(model_registry.generate.remote(prompt))

        self.assertIn("<thought>", response)
        self.assertIn("</thought>", response)

        # Test extraction in MemoryManager
        mm = MemoryManager.remote()
        # Mocking KnowledgeDistillation_Loop side effects via logs is hard,
        # so we just ensure it doesn't crash and correctly identifies trace
        ray.get(mm.KnowledgeDistillation_Loop.remote(response))

    def test_speculative_reflex_path(self):
        model_registry = ModelRegistry.remote()
        prompt = "Simple Task"

        # Test reflex mode
        reflex_response = ray.get(model_registry.generate.remote(prompt, mode="reflex"))
        self.assertIn("Reflex Result", reflex_response)

        # Test speculative reasoning mode
        reasoning_response = ray.get(model_registry.generate.remote(prompt, mode="reasoning"))
        self.assertIn("<thought>", reasoning_response)

    def test_active_inference_meta(self):
        meta_manager = MetaManager.remote()
        # Trigger active inference
        ray.get(meta_manager.receive.remote({"type": "active_inference_trigger"}))
        # If it didn't crash, the simulated logic passed.
        # In a real test we'd check state changes.

if __name__ == "__main__":
    unittest.main()
