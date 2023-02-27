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

def print_state(eng, b, n): # n = /4
    All(Measure) | b
    print('0x', end='')
    print_hex(eng, b, n)
    print('\n')

def print_hex(eng, qubits, n):
    for i in reversed(range(n)):
        temp = 0
        temp = temp+int(qubits[4*i+3])*8
        temp = temp+int(qubits[4*i+2])*4
        temp = temp+int(qubits[4*i+1])*2
        temp = temp+int(qubits[4*i])

        temp = hex(temp)
        y = temp.replace("0x", "")
        print(y, end='')

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

def bit_1_add(eng, a, b, carry):
    Toffoli_gate(eng, a, b, carry)
    CNOT | (a, b)

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

def CDKM(eng, a, b, c, n):
    for i in range(n - 2):
        CNOT | (a[i + 1], b[i + 1])

    CNOT | (a[1], c)
    Toffoli_gate(eng, a[0], b[0], c)
    CNOT | (a[2], a[1])
    Toffoli_gate(eng, c, b[1], a[1])
    CNOT | (a[3], a[2])

    for i in range(n - 5):
        Toffoli_gate(eng, a[i + 1], b[i + 2], a[i + 2])
        CNOT | (a[i + 4], a[i + 3])

    Toffoli_gate(eng, a[n - 4], b[n - 3], a[n - 3])
    CNOT | (a[n - 2], b[n - 1])
    CNOT | (a[n - 1], b[n - 1])
    Toffoli_gate(eng, a[n - 3], b[n - 2], b[n - 1])

    for i in range(n - 3):
        X | b[i + 1]

    CNOT | (c, b[1])

    for i in range(n - 3):
        CNOT | (a[i + 1], b[i + 2])

    Toffoli_gate(eng, a[n - 4], b[n - 3], a[n - 3])

    for i in range(n - 5):
        Toffoli_gate(eng, a[n - 5 - i], b[n - 4 - i], a[n - 4 - i])
        CNOT | (a[n - 2 - i], a[n - 3 - i])
        X | (b[n - 3 - i])

    Toffoli_gate(eng, c, b[1], a[1])
    CNOT | (a[3], a[2])
    X | b[2]
    Toffoli_gate(eng, a[0], b[0], c)
    CNOT | (a[2], a[1])
    X | b[1]
    CNOT | (a[1], c)

    for i in range(n-1):
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

def Inc_func_no_reverse(eng, ancilla, v, n):
    #Toffoli_gate(eng, v[0], v[1], ancilla[0])
    #for i in range(n-3):
    #    Toffoli_gate(eng, ancilla[i], v[i+2], ancilla[i+1])
    CNOT | (v[0], v[1])
    for i in range(n-2):
        CNOT | (ancilla[i], v[i+2])
    X | v[0]

def Inc_n_is_1(eng, v):
    CNOT | (v[0], v[1])
    X | (v[0])

def print_vecotr(eng, element, length):
    All(Measure) | element
    for k in range(length):
        print(int(element[length - 1 - k]), end='')
    print()

def Adder_Test(eng):

    n = 5 # bit length
    s = eng.allocate_qureg(n)
    k = eng.allocate_qureg(n)
    ancilla = eng.allocate_qureg(n-1)
    input_carry = eng.allocate_qubit() # For CDKM adder

    #carry = eng.allocate_qubit() # sign bit
    constant_1 = eng.allocate_qureg(n-1) # constant(1) --> optimization target

    if(resource_check != 1):
        Round_constant_XOR(0x1e, s, n) # s - k
        Round_constant_XOR(0xf, k, n)

    if (resource_check != 1):
        print('s: ', end='')
        print_vecotr(eng, s, n)
        print('k: ', end='')
        print_vecotr(eng, k, n)

    # 2's complement of k
    sign = eng.allocate_qubit()
    k_complement = []
    for i in range(n):
        k_complement.append(k[i])
    k_complement.append(sign)

    # All(X) | k_complement
    for i in range(n):
        X | k_complement[i]

    # Unb_fan_out_adder(eng, constant_1, k_complement, carry, n)  # b = b+a (optimization target)
    if(n == 1):
        Inc_n_is_1(eng, k_complement)
    else:
        Inc_func_no_reverse(eng, constant_1, k_complement, n+1)

    # check sign of (s + (-k))
    if (n == 1):
        bit_1_add(eng, k_complement[0:n], s, k_complement[n])
    else:
        Gidney_adder(eng, k, s, ancilla, n)
        #Gidney_no_modular_adder(eng, k_complement[0:n], s, ancilla, k_complement[n], n)
        #Unb_fan_out_adder(eng, k_complement[0:n], s, k_complement[n], n) # b = b+a (Parallel target)
        #CDKM_no_modular(eng, k_complement[0:n], s, input_carry, k_complement[n], n)
    if (resource_check != 1):
        print('Check sign : ', end='')
        print_vecotr(eng, k_complement[n], 1)
        print('\nIf the sign is 0 -> Negative (i.e., k > s)')

    if(s_minus_k == 1):
        result = eng.allocate_qureg(n)

        if(parallel == 1):
            print('prepairing')
            ancillas = eng.allocate_qureg(n-1)
            for i in range(n-1):
                CNOT | (k_complement[n], ancillas[i])
            #for i in range(n-1):
            #    Toffoli_gate(eng, ancillas[i], s[i], result[i])
            #Toffoli_gate(eng, k_complement[n], s[n-1], result[n-1])
        #else:
        #    for i in range(n):
        #        Toffoli_gate(eng, k_complement[n], s[i], result[i])

        if (resource_check != 1):
            print('Max value : ', end='')
            print_vecotr(eng, result, n)

def recursive_divide(eng, a, b, count): # n >= 4
        for i in range(count):
            CNOT | (a[i], a[i+count])
            CNOT | (b[i], b[i+count])

global resource_check
global NCT # NOT CNOT Toffoli
global s_minus_k
global parallel

resource_check = 0
NCT = 1
s_minus_k = 1
parallel = 1

'''
Resource = ClassicalSimulator()
eng = MainEngine(Resource)
Adder_Test(eng)
eng.flush()
'''

#### For Gidney Adder Test####
eng = MainEngine()
n = 5 # bit length
s = eng.allocate_qureg(n)
k = eng.allocate_qureg(n)
ancilla = eng.allocate_qureg(n-1)
if(resource_check != 1):
    Round_constant_XOR(0b11111, s, n) # s - k
    Round_constant_XOR(0b10000, k, n)
Gidney_adder(eng, k, s, ancilla, n)
print_vecotr(eng,s,n)
#Adder_Test(eng)
eng.flush()

print()
resource_check = 1
NCT = 0
s_minus_k = 1
parallel = 1

Resource = ResourceCounter()
eng = MainEngine(Resource)
Gidney_adder(eng, k, s, ancilla, n)
#Adder_Test(eng)

print(Resource)
eng.flush()