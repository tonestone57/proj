
class InteractionProtocol:
    def mediate(self, sender, receiver, message):
        return {"from": sender, "to": receiver, "payload": message}
