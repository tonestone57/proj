import pytest
import numpy as np
import ray
from actors.search_actor import SearchActor
from core.drives import PIDController

def test_simd_shuffling_logic():
    # Mock workspace and scheduler
    actor = SearchActor.remote(None, None)

    # Test vector (128-dim)
    vec = [1.0] * 64 + [-1.0] * 64

    # Test binary_quantize
    # Use ray.get since SearchActor is @ray.remote
    packed = ray.get(actor.binary_quantize.remote(vec))
    assert packed.dtype == np.uint64
    assert len(packed) == 2
    assert packed[0] == (2**64 - 1)
    assert packed[1] == 0

    # Test simd_batch_hamming
    query = packed
    # 4 candidates: one identical, one opposite, two mixed
    c1 = packed
    c2 = np.array([0, 2**64-1], dtype=np.uint64)
    c3 = np.array([2**64-1, 2**64-1], dtype=np.uint64)
    c4 = np.array([0, 0], dtype=np.uint64)

    batch = np.array([c1, c2, c3, c4])
    scores = ray.get(actor.simd_batch_hamming.remote(query, batch))

    assert scores[0] == 128 # Identical
    assert scores[1] == 0   # Opposite
    assert scores[2] == 64  # Half match (bits 0-63)
    assert scores[3] == 64  # Half match (bits 64-127)

def test_pid_controller():
    pid = PIDController(setpoint=72.0, kp=0.1, ki=0.01, kd=0.01)

    # Temp at setpoint
    assert pid.update(72.0) == 0.0

    # Temp above setpoint
    out1 = pid.update(75.0)
    assert out1 > 0.0

    # Temp rising
    out2 = pid.update(78.0)
    assert out2 > out1

    # Temp falling but still above setpoint
    out3 = pid.update(74.0)
    # Integral and Proportional still positive, but derivative is negative
    # Depending on gains, it should still be > 0
    assert out3 >= 0.0

if __name__ == "__main__":
    ray.init(ignore_reinit_error=True)
    try:
        test_simd_shuffling_logic()
        print("SIMD Shuffling Test Passed")
        test_pid_controller()
        print("PID Controller Test Passed")
    finally:
        ray.shutdown()
