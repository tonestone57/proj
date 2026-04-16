Grounded in the cognitive architecture research showing robots can develop synthetic episodic & autobiographical memory and a narrative self. royalsocietypublishing.org pmc.ncbi.nlm.nih.gov
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
This implements episodic → semantic AM, consistent with neuroimaging findings. MDPI