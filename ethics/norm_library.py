Stores ethical rules, norms, and constraints.
class NormLibrary:
    def __init__(self):
        self.norms = {
            "do_no_harm": {"weight": 1.0, "type": "constraint"},
            "fairness": {"weight": 0.8, "type": "value"},
            "reciprocity": {"weight": 0.6, "type": "value"},
            "honesty": {"weight": 0.7, "type": "value"},
            "autonomy_respect": {"weight": 0.9, "type": "constraint"}
        }

    def get_norms(self):
        return self.norms
This is the AGI’s ethical knowledge base.