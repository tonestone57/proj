import re

class TransparencyEngine:
    def generate_explanation(self, reasoning_trace, decision):
        # SGI 2026: Extract key arguments from reasoning trace
        trace_str = str(reasoning_trace)

        # Simple extraction of "because" or "since" clauses (simulated)
        arguments = re.findall(r"(?:because|since|due to)\s+([^,.]+)", trace_str, re.IGNORECASE)

        # Determine confidence based on presence of thought tags and length
        has_tags = "<thought>" in trace_str
        confidence = min(1.0, len(trace_str) / 500.0)
        if has_tags: confidence = min(1.0, confidence + 0.2)

        return {
            "decision": decision,
            "justification": trace_str,
            "key_arguments": arguments if arguments else ["Length-based justification"],
            "confidence": confidence,
            "verifiability": "high" if has_tags else "medium"
        }
