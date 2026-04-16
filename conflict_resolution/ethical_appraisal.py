Grounded in AGI Development Pathways’ emphasis on ethical accountability and societal consequences. Nature pmc.ncbi.nlm.nih.gov
class EthicalAppraisal:
    def evaluate(self, action, context):
        if context.get("harm", False):
            return {"ethical": False, "reason": "harm"}
        return {"ethical": True}