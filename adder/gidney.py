# https://quantum-journal.org/papers/q-2018-06-18-74/pdf/

import cirq
from cirq import H, CNOT, T, measure, S, CZ, NamedQubit, Circuit, X

#Gidney Adder

def logical_and(i,t,c):
    yield [H(c)]
    yield [T(c)]
    yield [CNOT(i,c), CNOT(t,c)]
    yield [CNOT(c,i), CNOT(c,t)]
    yield cirq.Moment((T ** -1)(i), (T ** -1)(t), T(c))
    yield [CNOT(c,i), CNOT(c,t)]
    yield [H(c)]
    yield [S(c)]

def logical_and_reverse(i,t,c):
    yield [H(c)]
    yield [measure(c, key=c.name)]
    yield [CZ(i,t).with_classical_controls(c.name)]

def Round_constant_XOR(circuit, rc, qubits, n):
    for i in range(n):
        if ((rc >> i) & 1):
            circuit.append(X(qubits[i]))

class Adder:
    def __init__(self, a, b):
        self.A, self.B = a, b
        self.circuit, self.result = self.construct_circuit()

    def construct_circuit(self):
        n = len(self.A)
        C = [NamedQubit("C" + str(i)) for i in range(n)]
        operations = []

        for k in range(n):
            if(k==0):
                operations.append(logical_and(self.A[k], self.B[k], C[k]))

            else:
                operations.append([CNOT(C[k-1], self.A[k]), CNOT(C[k-1], self.B[k])])
                if(k!=n-1):
                    operations.append(logical_and(self.A[k], self.B[k], C[k]))
                    operations.append(CNOT(C[k-1], C[k]))
                else:
                    operations.append(logical_and(self.A[k], self.B[k], C[-1]))
                    operations.append(CNOT(C[k-1], C[-1]))
                    operations.append(CNOT(C[k-1], self.A[k]))

        for k in reversed(range(n-1)):
            if(k==0):
                operations.append(logical_and_reverse(self.A[k], self.B[k], C[k]))
            else:
                operations.append(CNOT(C[k-1], C[k]))
                operations.append(logical_and_reverse(self.A[k], self.B[k], C[k]))
                operations.append(CNOT(C[k-1], self.A[k]))

        operations.append(CNOT(self.A[k], self.B[k]) for k in range(n))

        circuit = cirq.Circuit()
        circuit.append(operations)

        # measure
        #circuit.append(measure(self.carry,key='carry'))
        result = []
        for k in self.B:
            result.append(k)
        result.append(C[-1])
        #circuit.append(measure(result, key='result'))

        return circuit, result

'''
def adder_test(a, b, n):
    A = [NamedQubit("A" + str(i)) for i in range(n)]
    B = [NamedQubit("B" + str(i)) for i in range(n)]


    circuit = Circuit()
    Round_constant_XOR(circuit, a, A, n)  # 숫자, 큐빗, 길이
    Round_constant_XOR(circuit, b, B, n)
    adder = Adder(A, B)
    circuit.append(adder.circuit)
    circuit.append(cirq.measure(adder.result, key='result'))
    return circuit

n = 7
a = 3
b = 1

s = cirq.Simulator()
circuit=adder_test(a,b,n)

print('Simulate the circuit:')
results = s.simulate(circuit)

sum = []
#sum.append(results.measurements['carry'][0]) # 최상위비트 붙이기

print(results.measurements['result'])
#print(results.measurements)
#print(circuit)
'''