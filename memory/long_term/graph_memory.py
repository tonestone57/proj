import re
import ray

@ray.remote
class KnowledgeGraph:
    """
    GraphRAG implementation for connecting the dots across a project.
    Stores nodes (modules, classes, functions) and their relationships.
    """
    def __init__(self):
        self.nodes = {}  # id -> metadata
        self.edges = []  # list of (source, target, relationship_type)

    def add_node(self, node_id, metadata=None):
        if node_id not in self.nodes:
            self.nodes[node_id] = metadata or {}

    def add_edge(self, source, target, rel_type):
        self.add_node(source)
        self.add_node(target)
        edge = (source, target, rel_type)
        if edge not in self.edges:
            self.edges.append(edge)

    def query_connections(self, node_id):
        """Finds all direct dependencies or usages of a node."""
        connections = [edge for edge in self.edges if edge[0] == node_id or edge[1] == node_id]
        return connections

    def get_context_subgraph(self, node_id, depth=1):
        """Simulates finding a relevant subgraph for context enhancement."""
        related_nodes = {node_id}
        for _ in range(depth):
            new_nodes = set()
            for source, target, _ in self.edges:
                if source in related_nodes: new_nodes.add(target)
                if target in related_nodes: new_nodes.add(source)
            related_nodes.update(new_nodes)

        subgraph_edges = [edge for edge in self.edges if edge[0] in related_nodes and edge[1] in related_nodes]
        return {"nodes": list(related_nodes), "edges": subgraph_edges}

    def analyze_python_file(self, filepath, content):
        """Basic regex-based AST analysis to build the graph."""
        module_name = filepath.replace("/", ".").replace(".py", "")
        self.add_node(module_name, {"type": "module", "path": filepath})

        # Find classes
        classes = re.findall(r"class\s+(\w+)(?:\((.*?)\))?:", content)
        for class_name, base_classes in classes:
            full_class_name = f"{module_name}.{class_name}"
            self.add_node(full_class_name, {"type": "class"})
            self.add_edge(module_name, full_class_name, "contains")

            if base_classes:
                for base in base_classes.split(","):
                    base = base.strip()
                    self.add_edge(full_class_name, base, "inherits_from")

        # Find function definitions
        functions = re.findall(r"def\s+(\w+)\(.*\):", content)
        for func_name in functions:
            full_func_name = f"{module_name}.{func_name}"
            self.add_node(full_func_name, {"type": "function"})
            self.add_edge(module_name, full_func_name, "contains")

        # Find function calls (crude approximation)
        calls = re.findall(r"(\w+)\s*\(", content)
        for call in calls:
            if call not in ["print", "len", "range", "int", "str", "list", "dict", "set", "super", "self"]:
                # We don't know the full path of the called function easily without full AST/Symbol Table
                # But we can store the intent
                self.add_edge(module_name, call, "calls_potentially")
