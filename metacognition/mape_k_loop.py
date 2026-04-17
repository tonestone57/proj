Implements the classic Monitor–Analyze–Plan–Execute + Knowledge loop from autonomic computing.
This is the most battle-tested adaptive control pattern.
class MAPEKLoop:
    def cycle(self, monitor, analyze, plan, execute):
        m = monitor()
        a = analyze(m)
        p = plan(a)
        return execute(p)
MAPE-K is directly applicable to metacognitive AGI architectures.
zylos.ai