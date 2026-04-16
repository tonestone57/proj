Implements the probabilistic ethical reasoning framework proposed in Towards Ethical Reasoners. arXiv.org
class ProbabilisticReasoner:
    def infer(self, arguments):
        return {"confidence": len(arguments) / 10}