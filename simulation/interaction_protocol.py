Implements message-passing mediation (no direct agent-to-agent interference).
api.emergentmind.com
class InteractionProtocol:
    def mediate(self, sender, receiver, message):
        return {"from": sender, "to": receiver, "payload": message}