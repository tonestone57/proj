class TransparencyEngine:
    def generate_explanation(self, reasoning_trace, decision):
        return {
            "decision": decision,
            "justification": reasoning_trace,
            "confidence": len(reasoning_trace)
        }
