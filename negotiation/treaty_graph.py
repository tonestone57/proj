class TreatyGraph:
    def __init__(self):
        self.treaties = []

    def formulate(self, proposal):
        treaty = f"Treaty based on: {proposal.content}"
        self.treaties.append(treaty)
        return treaty
