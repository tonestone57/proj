class AutobiographicalMemory:
    def __init__(self):
        self.episodes = []
        self.semantic_summary = {}

    def store_episode(self, event):
        self.episodes.append(event)

    def summarize(self):
        summary = {}
        for ep in self.episodes:
            for k, v in ep.get("tags", {}).items():
                summary[k] = summary.get(k, 0) + v
        self.semantic_summary = summary
        return summary

    def retrieve(self, n=5):
        return self.episodes[-n:]
