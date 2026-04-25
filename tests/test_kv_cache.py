import unittest
import os
import shutil
import collections
from memory.memory_manager import KVCacheManager

class TestKVCache(unittest.TestCase):
    def setUp(self):
        self.storage_path = "./data/test_kv_cache_offload"
        if os.path.exists(self.storage_path):
            shutil.rmtree(self.storage_path)
        self.manager = KVCacheManager(max_active_blocks=3, storage_path=self.storage_path)

    def tearDown(self):
        if os.path.exists(self.storage_path):
            shutil.rmtree(self.storage_path)

    def test_paged_allocation_and_sharing(self):
        # Set block size to match prompt exactly for testing
        self.manager.block_size = 3
        prompt = ["SYSTEM", "AI", "Assistant"]
        req1_tokens = prompt + ["Help", "me"]
        req2_tokens = prompt + ["Code", "this"]

        b1 = self.manager.allocate_request("req1", req1_tokens)
        b2 = self.manager.allocate_request("req2", req2_tokens)

        # First block (containing "SYSTEM", "AI", "Assistant") should be shared
        self.assertEqual(b1[0], b2[0])
        # Second blocks should be different
        self.assertNotEqual(b1[1], b2[1])

        status = self.manager.get_status()
        self.assertGreaterEqual(status["shared_blocks"], 1)

    def test_lru_paged_eviction(self):
        # Fill RAM with UNIQUE blocks
        for i in range(5):
            self.manager.allocate_request(f"req{i}", [f"token{i}"] * 16)

        status = self.manager.get_status()
        self.assertEqual(status["active_blocks"], 3) # max_active_blocks is 3 in setUp
        self.assertEqual(status["offloaded_blocks"], 2)

    def test_retrieve_and_reload(self):
        self.manager.allocate_request("req1", ["data1"] * 16)
        self.manager.allocate_request("req2", ["data2"] * 16)
        self.manager.allocate_request("req3", ["data3"] * 16)
        self.manager.allocate_request("req4", ["data4"] * 16) # req1 evicted

        # Retrieve req1, should reload blocks
        kv = self.manager.get_kv_for_request("req1")
        self.assertIn("data1", str(kv))

        status = self.manager.get_status()
        self.assertEqual(status["active_blocks"], 3)

if __name__ == "__main__":
    unittest.main()
