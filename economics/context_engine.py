Implements context-aware coordination (traffic, weather, load, etc.) as in the EV-charging study.
class ContextEngine:
    def adjust(self, demand, context):
        if context.get("peak_load", False):
            return demand * 0.8
        return demand