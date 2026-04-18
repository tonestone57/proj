class VersionManager:
    def __init__(self):
        self.versions = {}

    def record_version(self, agent_id, version):
        self.versions.setdefault(agent_id, []).append(version)

    def latest(self, agent_id):
        return self.versions.get(agent_id, [])[-1]
