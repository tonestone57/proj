import time

class FastPathLZ4:
    """
    Simulates Flash-Optimized LZ4 compression for Tier 1 (Ephemeral) storage.
    Focuses on sub-millisecond latency for the Reflex Arc.
    """
    def __init__(self):
        self.latency_target = 0.0001  # 0.1ms target

    def compress(self, data):
        start_time = time.perf_counter()
        # Simulated LZ4 compression logic
        compressed = f"lz4_compressed({data[:10]}...)"

        # Simulate flash-optimized sub-millisecond latency
        time.sleep(max(0, self.latency_target - (time.perf_counter() - start_time)))

        print(f"[FastPathLZ4] Compressed in {(time.perf_counter() - start_time)*1000:.4f}ms")
        return compressed

    def decompress(self, compressed_data):
        start_time = time.perf_counter()
        # Simulated LZ4 decompression logic
        decompressed = "original_message_data"

        # Simulate flash-optimized sub-millisecond latency
        time.sleep(max(0, self.latency_target - (time.perf_counter() - start_time)))

        print(f"[FastPathLZ4] Decompressed in {(time.perf_counter() - start_time)*1000:.4f}ms")
        return decompressed
