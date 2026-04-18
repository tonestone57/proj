class MoralAgent:
    def __init__(self, domain):
        self.domain = domain

    def argue(self, scenario):
        return {"domain": self.domain, "argument": f"Analysis from {self.domain}"}
