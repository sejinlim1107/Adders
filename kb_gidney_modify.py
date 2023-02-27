# 230226 수정
# n=1일 때 문제 생겨서 수정함
from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap, Z, T, Tdag, S, Tdagger
from projectq.backends import CircuitDrawer, ResourceCounter, CommandPrinter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control, Dagger


def logical_and(eng, i, t, c):
    H | c
    T | c
    CNOT | (i, c)
    CNOT | (t, c)
    CNOT | (c, i)
    CNOT | (c, t)
    Tdag | i
    Tdag | t
    T | c
    CNOT | (c, i)
    CNOT | (c, t)
    H | c
    S | c

def logical_and_reverse(eng, i, t, c):
    H | c
    Measure | c
    ##
    if(int(c)):
        with Control(eng, i):
            Z | t
def Gidney_no_modular_adder(eng, a, b, c, n): # Generic Adder
    for k in range(n):
        if (k == 0):
            logical_and(eng, a[k], b[k], c[k])

        else:
            CNOT | (c[k - 1], a[k])
            CNOT | (c[k - 1], b[k])
            logical_and(eng, a[k], b[k], c[k])
            CNOT | (c[k - 1], c[k])
            if (k == n - 1):
                CNOT | (c[k - 1], a[k])

    for k in reversed(range(n - 1)):
        if (k == 0):
            logical_and_reverse(eng, a[k], b[k], c[k])

        else:
            CNOT | (c[k - 1], c[k])
            logical_and_reverse(eng, a[k], b[k], c[k])
            CNOT | (c[k - 1], a[k])

    for k in range(n):
        CNOT | (a[k], b[k])