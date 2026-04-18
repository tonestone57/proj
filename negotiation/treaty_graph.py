class TreatyGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_treaty(self, treaty):
        self.nodes.append(treaty)

    def add_dependency(self, t1, t2):
        self.edges.append((t1, t2))
