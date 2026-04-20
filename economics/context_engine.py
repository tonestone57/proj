class ContextEngine:
    def adjust(self, demand, context):
        if context.get("peak_load", False):
            return demand * 0.8
        return demand
