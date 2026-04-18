class EthicsManager:
    def __init__(self, norm_library):
        self.norm_library = norm_library

    def is_safe(self, message):
        # Placeholder logic: Check if message data contains 'harm'
        data = str(message.get("data", ""))
        if "harm" in data.lower() or "kill" in data.lower():
            return False
        return True
