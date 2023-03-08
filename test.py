# projectQ로 했던 것

from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap, Z, T, Tdag, S, Tdagger
from projectq.backends import CircuitDrawer, ResourceCounter, CommandPrinter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control, Dagger
from math import floor, ceil, log10, log2

def MAJ(eng,a,b,c):
    CNOT | (a, b)
    CNOT | (a, c)
    Toffoli_gate(eng, c,  b, a)

def UMA(eng,a,b,c):
    Toffoli_gate(eng, c,  b, a)
    CNOT | (c, b)
    CNOT | (a, c)

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

def Round_constant_XOR(rc, qubits, n):
    for i in range(n):
        if ((rc >> i) & 1):
            X | qubits[i]

def Toffoli_gate(eng, a, b, c):

    if (NCT):
        Toffoli | (a, b, c)
    else:
        if(resource_check ==1):
            Tdag | a
            Tdag | b
            H | c
            CNOT | (c, a)
            T | a
            CNOT | (b, c)
            CNOT | (b, a)
            T  | c
            Tdag | a
            CNOT | (b, c)
            CNOT | (c, a)
            T | a
            Tdag | c
            CNOT | (b, a)
            H | c
        else:
            Toffoli | (a, b, c)

def Gidney_no_modular_adder(eng, a, b, c, n):

    for k in range(n):
        if(k == 0):
            logical_and(eng, a[k], b[k], c[k])

        else:
            CNOT | (c[k-1], a[k])
            CNOT | (c[k-1], b[k])
            logical_and(eng, a[k], b[k], c[k])
            CNOT | (c[k-1], c[k])
            if (k == n-1):
                CNOT | (c[k-1], a[k])

    for k in reversed(range(n-1)):
        if(k==0):
            logical_and_reverse(eng, a[k], b[k], c[k])

        else:
            CNOT | (c[k-1], c[k])
            logical_and_reverse(eng, a[k], b[k], c[k])
            CNOT | (c[k-1], a[k])

    for k in range(n):
        CNOT | (a[k], b[k])


def Gidney_adder(eng, a, b, c, n): # <= 6-bit only (Do not use now)
    for k in range(n-1):
        if(k == 0):
            logical_and(eng, a[k], b[k], c[k])
            CNOT | (c[k], a[k+1])
            CNOT | (c[k], b[k+1])
        if(k == n-2):
            logical_and(eng, a[k], b[k], c[k])
            CNOT | (c[k-1], c[k])
            CNOT | (c[k], b[k+1])
        if(k !=0 and k != n-2):
            logical_and(eng, a[k], b[k], c[k])
            CNOT | (c[k-1], c[k])
            CNOT | (c[k], b[k + 1])
            CNOT | (c[k], a[k + 1])

    for k in reversed(range(n-1)):
        if(k==0):
            logical_and_reverse(eng, a[k], b[k], c[k])
        else:
            CNOT | (c[k-1], c[k])
            logical_and_reverse(eng, a[k], b[k], c[k])
            CNOT | (c[k-1], a[k])
    for k in range(n):
        CNOT | (a[k], b[k])
def print_vecotr(eng, element, length):
    All(Measure) | element
    for k in range(length):
        print(int(element[length - 1 - k]), end='')
    print()

def Unb_fan_out_adder(eng, a, b, carry, n):
    for i in range(1, n):
        CNOT | (a[i], b[i])
    CNOT | (a[n-1], carry)
    for i in range(n-2, 0, -1):
        CNOT | (a[i], a[i+1])
    for i in range(n-1):
        Toffoli_gate(eng, b[i], a[i], a[i+1])
    Toffoli_gate(eng, b[n-1], a[n-1], carry)
    for i in range(n-1, 0, -1):
        CNOT | (a[i], b[i])
        Toffoli_gate(eng, b[i-1], a[i-1], a[i])
    for i in range(1, n-1):
        CNOT | (a[i], a[i+1])
    for i in range(n):
        CNOT | (a[i], b[i])

def CDKM_no_modular(eng, a, b, c, z, n):
    for i in range(1, n):
        CNOT | (a[i], b[i])

    CNOT | (a[1], c)
    Toffoli_gate(eng, a[0], b[0], c)
    CNOT | (a[2], a[1])
    Toffoli_gate(eng, c, b[1], a[1])
    CNOT | (a[3], a[2])

    for i in range(2, n - 2):
        Toffoli_gate(eng, a[i - 1], b[i], a[i])
        CNOT | (a[i + 2], a[i + 1])

    Toffoli_gate(eng, a[n - 3], b[n - 2], a[n - 2])
    CNOT | (a[n - 1], z)
    Toffoli_gate(eng, a[n - 2], b[n - 1], z)

    for i in range(1, n - 1):
        X | (b[i])

    CNOT | (c, b[1])
    for i in range(2, n):
        CNOT | (a[i - 1], b[i])

    Toffoli_gate(eng, a[n - 3], b[n - 2], a[n - 2])

    for i in range(n - 3, 1, -1):
        Toffoli_gate(eng, a[i - 1], b[i], a[i])
        CNOT | (a[i + 2], a[i + 1])
        X | (b[i + 1])

    Toffoli_gate(eng, c, b[1], a[1])
    CNOT | (a[3], a[2])
    X | (b[2])

    Toffoli_gate(eng, a[0], b[0], c)
    CNOT | (a[2], a[1])
    X | (b[1])

    CNOT | (a[1], c)

    for i in range(0, n):
        CNOT | (a[i], b[i])

def AND_Test(eng):
    n = 1 # bit length
    s = eng.allocate_qureg(n)
    k = eng.allocate_qureg(n)
    ancilla = eng.allocate_qureg(n)

    if(resource_check != 1):
        Round_constant_XOR(0b1, s, n) # s - k
        Round_constant_XOR(0b0, k, n)

    print('s: ', end='')
    print_vecotr(eng, s, n)
    print('k: ', end='')
    print_vecotr(eng, k, n)
    print('c: ', end='')
    print_vecotr(eng, ancilla, n)
    logical_and(eng,s,k,ancilla)
    print('after AND')
    print('s: ', end='')
    print_vecotr(eng, s, n)
    print('k: ', end='')
    print_vecotr(eng, k, n)
    print('c: ', end='')
    print_vecotr(eng, ancilla, n)
    logical_and_reverse(eng,s,k,ancilla)
    print('after reverse_AND')
    print('s: ', end='')
    print_vecotr(eng, s, n)
    print('k: ', end='')
    print_vecotr(eng, k, n)
    print('c: ', end='')

def adder_test(eng):
    n = 5  # bit length
    s = eng.allocate_qureg(n)
    k = eng.allocate_qureg(n)
    ancilla = eng.allocate_qubit()
    z = eng.allocate_qubit()

    #CDKM_no_modular(eng, s, k, ancilla,z, n)

    Unb_fan_out_adder(eng, s, k, ancilla, n)

'''
resource_check = 0
NCT = 1
Resource = ClassicalSimulator()
eng = MainEngine(Resource)
Adder_Test(eng)
eng.flush()
'''

'''
#### For Gidney Adder Test####
eng = MainEngine()
AND_Test(eng)
#Adder_Test(eng)
eng.flush()
'''

print()
resource_check = 1
NCT = 1


Resource = ResourceCounter()
eng = MainEngine(Resource)

adder_test(eng)

print(Resource)
eng.flush()
