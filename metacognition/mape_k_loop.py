import ray
from core.base import CognitiveModule

@ray.remote # SGI 2026: Standardized Ray Actor
class MAPEKLoop(CognitiveModule):
    def cycle(self, monitor, analyze, plan, execute):
        m = monitor()
        a = analyze(m)
        p = plan(a)
        return execute(p)
