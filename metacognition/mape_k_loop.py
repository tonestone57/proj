import ray
from core.base import CognitiveModule

@ray.remote
class MAPEKLoop(CognitiveModule):
    def cycle(self, monitor, analyze, plan, execute):
        m = monitor()
        a = analyze(m)
        p = plan(a)
        return execute(p)
