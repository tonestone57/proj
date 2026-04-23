class ConsensusController:
    def combine(self, monitor_data, reasoner_data):
        # SGI 2026: Multi-signal metacognitive integration
        monitor_score = monitor_data.get("metrics", {}).get("efficiency", 1.0)
        reasoner_score = reasoner_data.get("score", 0.5)

        combined = (monitor_score * 0.4) + (reasoner_score * 0.6)

        return {
            "meta_score": combined,
            "status": "coherent" if abs(monitor_score - reasoner_score) < 0.5 else "dissonant"
        }
