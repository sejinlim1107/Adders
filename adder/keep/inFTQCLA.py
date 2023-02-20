#IN-PLACE QCLA CIRCUITS 1
#https://arxiv.org/pdf/2004.01826.pdf

import cirq
import math as mt
import utils.counting_utils as cu

def uncomputation(x, y, xy):
    yield [cirq.H(xy)]
    yield [cirq.measure(xy, key=xy.name)]
    yield [cirq.CZ(x, y).with_classical_controls(xy.name)]

# logical-AND gate
def logicalAND(x, y, A):
    yield [cirq.CNOT(x, A)]
    yield [cirq.CNOT(y, A)]
    yield [cirq.CNOT(A, x),cirq.CNOT(A, y)]
    yield [(cirq.T**-1)(x), (cirq.T**-1)(y), cirq.T(A)]
    yield [cirq.CNOT(A, x), cirq.CNOT(A,y)]
    yield [cirq.H(A)]
    yield [cirq.S(A)]


class LogicalAND(cirq.Gate):
    def __init__(self):
        super(LogicalAND, self)

    def _num_qubits_(self):
        return 3

    def _decompose_(self, qubits):
        x, y, A = qubits

        yield [cirq.CNOT(x, A)]
        yield [cirq.CNOT(y, A)]
        yield [cirq.CNOT(A, x), cirq.CNOT(A, y)]
        yield [(cirq.T ** -1)(x), (cirq.T ** -1)(y), cirq.T(A)]
        yield [cirq.CNOT(A, x), cirq.CNOT(A, y)]
        yield [cirq.H(A)]
        yield [cirq.S(A)]

    def _circuit_diagram_info_(self, args):
        return "@","@","*"

class Uncomputation(cirq.Gate):
    def __init__(self):
        super(Uncomputation, self)

    def _num_qubits_(self):
        return 3

    def _decompose_(self, qubits):
        x, y, xy = qubits

        yield [cirq.H(xy)]
        yield [cirq.measure(xy,key=xy.name)]
        yield [cirq.CZ(x, y).with_classical_controls(xy.name)]


    def _circuit_diagram_info_(self, args):
        return "@","@","="

class LogicalAND(cirq.Gate):
    def __init__(self):
        super(LogicalAND, self)

    def _num_qubits_(self):
        return 3

    def _decompose_(self, qubits):
        x, y, A = qubits

        yield [cirq.CNOT(x, A)]
        yield [cirq.CNOT(y, A)]
        yield [cirq.CNOT(A, x), cirq.CNOT(A, y)]
        yield [(cirq.T ** -1)(x), (cirq.T ** -1)(y), cirq.T(A)]
        yield [cirq.CNOT(A, x), cirq.CNOT(A, y)]
        yield [cirq.H(A)]
        yield [cirq.S(A)]

    def _circuit_diagram_info_(self, args):
        return "@","@","*"




class CarryLookaheadAdder:
    def __init__(self, A, B, t=1):
        self.A, self.B = A, B
        self.t = t
        self.circuit, self.result = self.construct_circuit()

    def w(self,x):
        return x - sum(int(mt.floor(x / (mt.pow(2, y)))) for y in range(1, int(mt.log2(x)) + 1))

    def construct_circuit(self):
        if(self.t>2):
            return
        n = len(self.A)

        init = []
        step1 = []
        step2 = []
        step3 = []
        step4 = []
        step5 = []
        step6 = []
        step7 = []
        step8 = []
        step9 = []
        step10 = []
        step11 = []
        step12 = []
        step13 = []
        step14 = []
        step15 = []
        step16 = []

        #init ancilla
        #ancilla_num = 4* n - 2 * self.w(n) - 2 * mt.floor(mt.log2(n))
        ancilla_num = n + 1 + 3 * n - 2 * self.w(n) - 2 * mt.floor(mt.log2(n)) + 2*n - self.w(n-1) - mt.floor(mt.log2(n-1)) -3
        if(self.t==2):
            ancilla_num = n + n - self.w(n) - mt.floor(mt.log2(n)) + 1

        #ancilla_num = 3 * n - 2 * self.w(n) - 2 * mt.floor(mt.log2(n))

        ancilla = [cirq.NamedQubit("a" + str(i)) for i in range(ancilla_num)]

        init.append(cirq.H(ancilla[i]) for i in range(ancilla_num))
        init.append(cirq.T(ancilla[i]) for i in range(ancilla_num))

        #step 1
        for i in range(n):
            step1.append(logicalAND(self.A[i], self.B[i], cirq.NamedQubit(str("a"+str(i)))))

        # ancilla -> g[i, i +1]
        g = {}
        for i in range(n):
            g[str(i) + "," + str(i + 1)] = cirq.NamedQubit(str("a" + str(i)))

        # step 2 paper error
        for i in range(0, n):
            step2.append(cirq.CNOT(self.A[i], self.B[i]))

        # B[i] -> p[i, i+1]
        p = {}
        for i in range(0,n):
            p[str(i) + "," + str(i + 1)] = cirq.NamedQubit(str("B" + str(i)))

        # step 3 (P-rounds)
        num=n
        for t in range(1, mt.floor(mt.log2(n))):
            for m in range(1, mt.floor(n / mt.pow(2, t))):
                j = int(mt.pow(2, t) * m)
                k = int(mt.pow(2, t) * m + (mt.pow(2, t)))
                l = int(mt.pow(2, t) * m + (mt.pow(2, t - 1)))
                step3.append(logicalAND(p[str(str(j)+","+str(l))], p[str(str(l)+","+str(k))], cirq.NamedQubit(str("a" + str(num)))))
                p[str(j) + "," + str(k)] = cirq.NamedQubit(str("a" + str(num)))

                num+=1


        #Step 4 (G-rounds)
        for t in range(1, mt.floor(mt.log2(n))+1):
            for m in range(0, mt.floor(n / mt.pow(2, t))):
                j = int(mt.pow(2, t) * m)
                k = int(mt.pow(2, t) * m + (mt.pow(2, t)))
                l = int(mt.pow(2, t) * m + (mt.pow(2, t - 1)))

                if (self.t == 1):
                    step4.append(logicalAND(g[str(str(j) + "," + str(l))], p[str(str(l) + "," + str(k))],
                                              cirq.NamedQubit(str("a" + str(num)))))
                    step4.append(cirq.CNOT(cirq.NamedQubit(str("a" + str(num))), g[str(str(l) + "," + str(k))]))
                    step4.append(uncomputation(g[str(str(j) + "," + str(l))], p[str(str(l) + "," + str(k))],
                                                 cirq.NamedQubit(str("a" + str(num)))))

                    num += 1
                
                if (self.t == 2):
                    step4.append(cirq.TOFFOLI(g[str(str(j) + "," + str(l))], p[str(str(l) + "," + str(k))], g[str(str(l) + "," + str(k))]))


                g[str(str(j) + "," + str(k))] = g.pop(str(str(l) + "," + str(k)))


        #Step 5 (C-rounds)
        for t in reversed(range(1,mt.floor(mt.log2(2*n/3))+1)):
            for m in range(1, mt.floor(((n-mt.pow(2, t-1)) /mt.pow(2, t)))+1):
                l = int(mt.pow(2, t)*m)
                k = int(mt.pow(2, t)*m + mt.pow(2, t-1))

                if (self.t == 1):
                    step5.append(logicalAND(g[str(str(0) + "," + str(l))], p[str(str(l) + "," + str(k))], cirq.NamedQubit(str("a" + str(num)))))

                    step5.append(cirq.CNOT(cirq.NamedQubit(str("a" + str(num))), g[str(str(l) + "," + str(k))]))
                    step5.append(uncomputation(g[str(str(0) + "," + str(l))], p[str(str(l) + "," + str(k))],
                                             cirq.NamedQubit(str("a" + str(num)))))

                    num += 1
                if (self.t == 2):
                    step5.append(cirq.TOFFOLI(g[str(str(0) + "," + str(l))], p[str(str(l) + "," + str(k))], g[str(str(l)+","+str(k))]))


                g[str(str(0) + "," + str(k))] = g.pop(str(str(l) + "," + str(k)))


        #Step 6 (P-erase-rounds)
        for t in reversed(range(1,mt.floor(mt.log2(n)))):
            for m in range(1, mt.floor(n/mt.pow(2,t))):
                j = int(mt.pow(2,t)*m)
                k = int(mt.pow(2,t)*m + mt.pow(2,t))
                l = int(mt.pow(2,t)*m + mt.pow(2,t-1))
                step6.append(uncomputation(p[str(str(j) + "," + str(l))], p[str(str(l) + "," + str(k))],p[str(str(j) + "," + str(k))]))


        # Step 7
        for i in range(1,n):
            step7.append(cirq.CNOT(g[str(str(0) + "," + str(i))], p[str(str(i) + "," + str(i+1))]))


        # Step 8
        step8.append(cirq.X(self.B[0]))
        p[str(0) + "," + str(1)] = self.B[0]
        for i in range(1,n-1):
            step8.append(cirq.X(p[str(i) + "," + str(i+1)]))


        # Step 9
        for i in range(1, n - 1):
            step9.append(cirq.CNOT(self.A[i], p[str(i) + "," + str(i + 1)]))


        # Step 10 (Reverse of P-erase-round)
        for t in range(1, mt.floor(mt.log2(n))):
            for m in range(1, mt.floor(n / mt.pow(2, t))):
                j = int(mt.pow(2, t) * m)
                k = int(mt.pow(2, t) * m + (mt.pow(2, t)))
                l = int(mt.pow(2, t) * m + (mt.pow(2, t - 1)))
                step10.append(logicalAND(p[str(str(j)+","+str(l))], p[str(str(l)+","+str(k))], cirq.NamedQubit(str("a" + str(num)))))
                p[str(j) + "," + str(k)] = cirq.NamedQubit(str("a" + str(num)))

                num+=1



        # Step 11 (Reverse of C-erase-round)
        for t in range(1,mt.floor(mt.log2(2*n/3))+1):
            for m in range(1, mt.floor((n-mt.pow(2, t-1)) /mt.pow(2, t))+1):
                l = int(mt.pow(2, t)*m)
                k = int(mt.pow(2, t)*m + mt.pow(2, t-1))

                if (self.t == 1):
                    step5.append(logicalAND(g[str(str(0) + "," + str(l))], p[str(str(l) + "," + str(k))], cirq.NamedQubit(str("a" + str(num)))))

                    step5.append(cirq.CNOT(cirq.NamedQubit(str("a" + str(num))), g[str(str(0) + "," + str(k))]))
                    step5.append(uncomputation(g[str(str(0) + "," + str(l))], p[str(str(l) + "," + str(k))],
                                             cirq.NamedQubit(str("a" + str(num)))))
                    num += 1
                if (self.t == 2):
                    step11.append(cirq.TOFFOLI(g[str(str(0) + "," + str(l))], p[str(str(l) + "," + str(k))], g[str(str(0)+","+str(k))]))


                g[str(str(l) + "," + str(k))] = g.pop(str(str(0) + "," + str(k)))


        # Step 12 (Reverse of G-erase-round)
        for t in reversed(range(1, mt.floor(mt.log2(n))+1)):
            for m in range(0, mt.floor(n / mt.pow(2, t))):
                j = int(mt.pow(2, t) * m)
                k = int(mt.pow(2, t) * m + (mt.pow(2, t)))
                l = int(mt.pow(2, t) * m + (mt.pow(2, t - 1)))

                if (self.t == 1):
                    step4.append(logicalAND(g[str(str(j) + "," + str(l))], p[str(str(l) + "," + str(k))],
                                              cirq.NamedQubit(str("a" + str(num)))))

                    step4.append(cirq.CNOT(cirq.NamedQubit(str("a" + str(num))), g[str(str(j) + "," + str(k))]))
                    step4.append(uncomputation(g[str(str(j) + "," + str(l))], p[str(str(l) + "," + str(k))],
                                                 cirq.NamedQubit(str("a" + str(num)))))
                    num += 1

                if (self.t == 2):
                    step12.append(cirq.TOFFOLI(g[str(str(j) + "," + str(l))], p[str(str(l) + "," + str(k))], g[str(str(j) + "," + str(k))]))

                g[str(str(l) + "," + str(k))] = g.pop(str(str(j) + "," + str(k)))


        # Step 13 (Reverse of P-erase-round)
        for t in reversed(range(1, mt.floor(mt.log2(n)))):
            for m in range(1, mt.floor((n-1) / mt.pow(2, t))):
                j = int(mt.pow(2, t) * m)
                k = int(mt.pow(2, t) * m + (mt.pow(2, t)))
                l = int(mt.pow(2, t) * m + (mt.pow(2, t - 1)))
                step13.append(uncomputation(p[str(str(j)+","+str(l))], p[str(str(l)+","+str(k))], p[str(str(j)+","+str(k))]))



        # Step 14
        for i in range(1, n-1):
            step14.append(cirq.CNOT(self.A[i], p[str(str(i)+","+str(i+1))]))

        # Step 15
        for i in range(1, n - 1):
            step15.append(uncomputation(self.A[i], p[str(str(i) + "," + str(i + 1))], g[str(str(i) + "," + str(i + 1))]))


        # Step 16
        for i in range(0, n - 1):
            step16.append(cirq.X(p[str(str(i) + "," + str(i + 1))]))

        circuit = cirq.Circuit()
        circuit.append(init)
        circuit.append(step1)

        circuit.append(step2)
        circuit.append(step3)
        circuit.append(step4)
        circuit.append(step5)
        circuit.append(step6)
        circuit.append(step7)
        circuit.append(step8)
        circuit.append(step9)
        circuit.append(step10)
        circuit.append(step11)
        circuit.append(step12)
        circuit.append(step13)
        circuit.append(step14)
        circuit.append(step15)
        circuit.append(step16)

        result = []
        for a in self.B:
            result.append(a)
        result.append(ancilla[n-1])

        #measure
        #circuit.append(cirq.measure(self.A, key='A'))

        #circuit.append(cirq.measure(result, key='result'))


        return circuit, result

'''
def add(a, b, n, t=2):

    A = [cirq.NamedQubit("A" + str(i)) for i in range(n)]
    B = [cirq.NamedQubit("B" + str(i)) for i in range(n)]


    circuit = cirq.Circuit()
    for i in range(n):
        if ((a >> i) & 1 == 1):
            circuit.append(cirq.X(A[i]))
        if ((b >> i) & 1 == 1):
            circuit.append(cirq.X(B[i]))
    circuit.append(CarryLookaheadAdder(A, B,t).circuit)


    return circuit

n=5
a=3
b=5
''''''

s = cirq.Simulator()
circuit=add(a,b,n)


print('Simulate the circuit:')
results = s.simulate(circuit)
print(results.measurements['result'])

#print(results.measurements)
#print(circuit)

print(f"T_depth : {int(cu.count_t_depth_of_circuit(circuit))}")
print(f"T_count : {int(cu.count_t_of_circuit(circuit))}")
print(f"Toffoli_depth : {int(cu.count_toffoli_depth_of_circuit(circuit))}")
print(f"Toffoli_count : {int(cu.count_toffoli_of_circuit(circuit))}")
print(f"CNOT_count : {int(cu.count_cnot_of_circuit(circuit))}")
print(f"H_count : {int(cu.count_h_of_circuit(circuit))}")
print(f"Qubit_count : {int(cirq.num_qubits(circuit))}")

'''