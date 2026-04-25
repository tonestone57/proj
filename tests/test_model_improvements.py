import unittest
from core.model_registry import NGramCache

class TestModelImprovements(unittest.TestCase):
    def test_multi_level_ngram_cache(self):
        cache = NGramCache(ns=[4, 3, 2])
        text = "this is a test of the emergency broadcast system"
        cache.update(text)

        # Test 4-gram match
        # "this is a test" -> "of"
        proposals = cache.propose("this is a test")
        self.assertIn("of", proposals)

        # Test 3-gram match (fallback)
        # "is a test" -> "of"
        proposals_3 = cache.propose("is a test")
        self.assertIn("of", proposals_3)

        # Test 2-gram match (fallback)
        # "a test" -> "of"
        proposals_2 = cache.propose("a test")
        self.assertIn("of", proposals_2)

    def test_lru_eviction(self):
        cache = NGramCache(ns=[2], max_size=2) # ns=[2] means it will store (prefix,) -> next, so it's 1-gram prefix.
        # Actually in my implementation, ns=2 means prefix is tuple of length 2.
        # So "a b c" -> (a,b) -> c
        cache = NGramCache(ns=[2], max_size=3) # max_size is per N-level (max_size // len(ns))
        # Wait, my implementation: len(cache) >= self.max_size // len(self.ns)
        # ns=[2] -> len(ns) = 1. max_size = 3.

        cache.update("a b c d e f")
        # Tuples stored: (a,b), (b,c), (c,d), (d,e)
        # If max_size=3, it should keep only (c,d), (d,e), (e,f) wait...
        # "a b c d e f"
        # i=0: (a,b) -> c
        # i=1: (b,c) -> d
        # i=2: (c,d) -> e
        # i=3: (d,e) -> f

        # If max_size=3, only 3 entries kept. (a,b) should be evicted.
        self.assertNotIn(("a", "b"), cache.caches[2])
        self.assertIn(("d", "e"), cache.caches[2])

    def test_symbolic_reflex_path(self):
        import ray
        from core.model_registry import PrimaryModelActor
        # Initialize without loading actual models for speed/memory
        registry = PrimaryModelActor.remote()

        # Test exact reflex match
        res = ray.get(registry.generate.remote("What is sym_int8"))
        self.assertIn("<reflex>", res)
        self.assertIn("symmetric 8-bit integer", res)

        # Test fuzzy reflex match (regex)
        res_fuzzy = ray.get(registry.generate.remote("Can you describe Tier 1?"))
        self.assertIn("<reflex>", res_fuzzy)
        self.assertIn("Symbolic Reflex", res_fuzzy)

if __name__ == "__main__":
    unittest.main()
