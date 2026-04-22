import unittest
import ray
from actors.search_actor import SearchActorBase
from core.workspace import GlobalWorkspace
from core.scheduler import Scheduler

class MockKnowledgeGraph:
    def __init__(self):
        self.nodes = {
            "actors/coding_actor.py": {"edges": ["defines:CodingActor", "imports:ray"]},
            "CodingActor.execute_logic_internal": {"edges": ["calls:detect_recursion", "calls:iterative_transform"]},
            "detect_recursion": {"edges": ["defined_in:actors/coding_actor.py"]},
            "module.function": {"edges": ["edge1:neighbor_node"]},
            "neighbor_node": {"edges": ["secondary_edge:target"]}
        }
    def get_context_subgraph(self, node):
        return self.nodes.get(node, {"edges": []})

class TestSearchImprovements(unittest.TestCase):
    def test_graphrag_node_extraction(self):
        # We don't need Ray for this logic test if we use the base class or mock carefully
        # But let's just test the regex and logic in SearchActor.receive

        graph = MockKnowledgeGraph()
        actor = SearchActorBase(None, None, graph_memory=graph)

        # Mock message
        class MockScheduler:
            def __init__(self):
                self.last_msg = None
            def submit(self, handle, msg):
                self.last_msg = msg

        actor.scheduler = MockScheduler()

        # Query with multi-file and complex patterns
        query = "What does CodingActor.execute_logic_internal do in actors/coding_actor.py? and module.function"

        # Manually trigger receive logic (or parts of it)
        # We want to see if it correctly identifies the nodes
        actor.receive({"type": "search_request", "data": query})

        spec = actor.scheduler.last_msg["actionable_spec"]
        self.assertIn("Related to actors/coding_actor.py", spec)
        self.assertIn("Related to CodingActor.execute_logic_internal", spec)
        self.assertIn("Related to module.function", spec)

        # Verify Multi-Hop traversal
        self.assertIn("Neighbor neighbor_node", spec)
        self.assertIn("secondary_edge:target", spec)

if __name__ == "__main__":
    unittest.main()
