import unittest
import sys
import os
import ray

# Add the repo root to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from actors.reasoner_actor import ReasonerActor

class TestReasonerSecurity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ray.init(ignore_reinit_error=True, num_cpus=1)

    @classmethod
    def tearDownClass(cls):
        ray.shutdown()

    def setUp(self):
        self.actor = ReasonerActor.remote(workspace=None, scheduler=None)

    def test_valid_math(self):
        result = ray.get(self.actor.reason.remote("2 + 2"))
        self.assertEqual(result, 4.0)

        result = ray.get(self.actor.reason.remote("sqrt(16)"))
        self.assertEqual(result, 4.0)

    def test_logical_operators(self):
        result = ray.get(self.actor.reason.remote("True and False"))
        self.assertEqual(str(result), "False")

        result = ray.get(self.actor.reason.remote("True or False"))
        self.assertEqual(str(result), "True")

    def test_injection_attempts(self):
        result = ray.get(self.actor.reason.remote("__import__('os').system('ls')"))
        self.assertTrue("Error" in result)

        result = ray.get(self.actor.reason.remote("self.__dict__"))
        self.assertTrue("Error" in result)

    def test_complex_math(self):
        result = ray.get(self.actor.reason.remote("sin(0) + cos(0)"))
        self.assertEqual(result, 1.0)

if __name__ == "__main__":
    unittest.main()
