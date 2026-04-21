import unittest
import ray
from actors.reasoner_actor import SymbolicReasonerLogic

class TestHybridReasoning(unittest.TestCase):
    def test_symbolic_success(self):
        # Math queries should succeed symbolically
        logic = SymbolicReasonerLogic()
        result = logic.reason("2 + 2")
        self.assertEqual(result, 4)

        result_math = logic.reason("math.sqrt(16)")
        self.assertEqual(result_math, 4.0)

    def test_symbolic_failure_logic(self):
        # Semantic queries should fail symbolically
        logic = SymbolicReasonerLogic()

        # "Who is the user?" cannot be solved by eval()
        result = logic.reason("Who is the user?")
        self.assertTrue(isinstance(result, str))
        self.assertTrue(result.startswith("Error"))

if __name__ == "__main__":
    unittest.main()
