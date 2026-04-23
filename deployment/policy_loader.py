import time

class PolicyLoader:
    def __init__(self):
        self.policies = {} # policy_name -> {data, loaded_at}

    def load(self, name, policy_data):
        # SGI 2026: Dynamic policy hot-reloading
        print(f"[PolicyLoader] Loading policy: {name} (v{policy_data.get('version', '1.0')})")

        entry = {
            "data": policy_data,
            "loaded_at": time.time(),
            "version": policy_data.get("version", "1.0")
        }
        self.policies[name] = entry

    def get(self, name):
        entry = self.policies.get(name)
        return entry["data"] if entry else None

    def list_versions(self):
        return {k: v["version"] for k, v in self.policies.items()}
