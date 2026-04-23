import z3
try:
    x = z3.Real('x')
    s = z3.Solver()
    s.add(x**2 == 9)
    t = z3.Tactic('nlsat')
    # This was the failing line in the trace
    res = t(s.assertions())
    print("Direct assertions call success:", res)
except Exception as e:
    print("Direct assertions call failed:", e)

try:
    x = z3.Real('x')
    s = z3.Solver()
    s.add(x**2 == 9)
    t = z3.Tactic('nlsat')
    g = z3.Goal()
    g.add(s.assertions())
    res = t(g)
    print("Goal call success:", res)
except Exception as e:
    print("Goal call failed:", e)
