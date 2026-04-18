class MAPEKLoop:
    def cycle(self, monitor, analyze, plan, execute):
        m = monitor()
        a = analyze(m)
        p = plan(a)
        return execute(p)
