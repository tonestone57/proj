class ProbabilisticReasoner:
    def infer(self, arguments):
        return {"confidence": len(arguments) / 10}
