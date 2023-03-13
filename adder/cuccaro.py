"""
Implementation of the carry ripple adder in the form presented by Cuccaro
in https://arxiv.org/pdf/quant-ph/0410184.pdf
"""

import cirq

class Adder:

    # 옵션 2가지. 2cnot / 3cnot

    def __init__(self, a, b, UMA_2_CNots=False):
        #print("Carry Ripple Adder")
        self.A, self.B = a, b
        self.nr_qubits = len(self.A)
        self.C = cirq.NamedQubit("c0")
        self.Z = cirq.NamedQubit("z0")

        if self.nr_qubits == 1:
            self.circuit, self.result = self.construct_circuit1()

        elif self.nr_qubits == 2:
            self.circuit, self.result = self.construct_circuit2()

        elif self.nr_qubits == 3:
            self.circuit, self.result = self.construct_circuit3()

        else: # n >= 4
            if UMA_2_CNots:
                self.circuit, self.result = self.construct_circuit_2cnot()
            else:
                self.circuit, self.result = self.construct_circuit_3cnot()

    def construct_circuit1(self):
        op = []
        op.append(cirq.TOFFOLI(self.B[0],self.A[0],self.Z))
        op.append(cirq.CNOT(self.A[0],self.B[0]))

        result = []
        result.append(self.B[0])
        result.append(self.Z)

        circuit = cirq.Circuit()
        circuit.append(op)

        return circuit, result

    def construct_circuit2(self):
        op = []
        op.append(cirq.CNOT(self.A[1],self.B[1]))
        op.append(cirq.CNOT(self.A[1],self.C))
        op.append(cirq.TOFFOLI(self.B[0],self.A[0],self.C))
        op.append(cirq.CNOT(self.A[1],self.Z))
        op.append(cirq.TOFFOLI(self.C,self.B[1],self.Z))
        op.append(cirq.CNOT(self.C,self.B[1]))
        op.append(cirq.TOFFOLI(self.B[0],self.A[0],self.C))
        op.append(cirq.CNOT(self.A[0], self.B[0]))
        op.append(cirq.CNOT(self.A[1], self.C))
        op.append(cirq.CNOT(self.A[1], self.B[1]))

        circuit = cirq.Circuit()
        circuit.append(op)

        result = []
        result.append(self.B[0])
        result.append(self.B[1])
        result.append(self.Z)

        return circuit, result

    def construct_circuit3(self):
        op = []
        op.append(cirq.CNOT(self.A[1],self.B[1]))
        op.append(cirq.CNOT(self.A[2],self.B[2]))
        op.append(cirq.CNOT(self.A[1],self.C))
        op.append(cirq.TOFFOLI(self.B[0],self.A[0],self.C))
        op.append(cirq.CNOT(self.A[2],self.A[1]))
        op.append(cirq.TOFFOLI(self.C,self.B[1],self.A[1]))
        op.append(cirq.CNOT(self.A[2],self.Z))
        op.append(cirq.X(self.B[1]))
        op.append(cirq.TOFFOLI(self.A[1],self.B[2],self.Z))
        op.append(cirq.CNOT(self.C, self.B[1]))
        op.append(cirq.CNOT(self.A[1], self.B[2]))
        op.append(cirq.TOFFOLI(self.C, self.B[1], self.A[1]))
        op.append(cirq.TOFFOLI(self.B[0],self.A[0],self.C))
        op.append(cirq.X(self.B[1]))
        op.append(cirq.CNOT(self.A[2], self.A[1]))
        op.append(cirq.CNOT(self.A[1], self.C))
        op.append(cirq.CNOT(self.A[2], self.B[2]))
        op.append(cirq.CNOT(self.A[0], self.B[0]))
        op.append(cirq.CNOT(self.A[1], self.B[1]))

        circuit = cirq.Circuit()
        circuit.append(op)

        result = []
        result.append(self.B[0])
        result.append(self.B[1])
        result.append(self.B[2])
        result.append(self.Z)

        return circuit, result

    '''
    def MAJ_gate(self, a, b, c):
        op = []

        op.append(cirq.CNOT(a, b))
        op.append(cirq.CNOT(a, c))
        op.append(cirq.TOFFOLI(c, b, a))

        return op

    def UMA_2cnot_gate(self, a, b, c):
        op = []

        op.append(cirq.TOFFOLI(c, b, a))
        op.append(cirq.CNOT(a, c))
        op.append(cirq.CNOT(c, b))

        return op

    
    def UMA_3cnot_gate(self, a, b, c):

        self.circuit.append(cirq.X.on(b))
        self.circuit.append(cirq.CNOT.on(c, b))
        self.circuit.append(cirq.TOFFOLI.on(c, b, a))
        self.circuit.append(cirq.X.on(b))
        self.circuit.append(cirq.CNOT.on(a, c))
        self.circuit.append(cirq.CNOT.on(a, b))
    '''

    def construct_circuit_3cnot(self): # Figure 5,6
        n = len(self.A)
        op = []

        op.append(cirq.CNOT(self.A[i],self.B[i]) for i in range(1,n))
        op.append(cirq.CNOT(self.A[1],self.C))
        op.append(cirq.TOFFOLI(self.A[0],self.B[0],self.C))
        op.append(cirq.CNOT(self.A[2],self.A[1]))
        op.append(cirq.TOFFOLI(self.C,self.B[1],self.A[1]))
        op.append(cirq.CNOT(self.A[3],self.A[2]))

        for i in range(2,n-2):
            op.append(cirq.TOFFOLI(self.A[i-1], self.B[i], self.A[i]))
            op.append(cirq.CNOT(self.A[i+2],self.A[i+1]))
        op.append(cirq.TOFFOLI(self.A[n-3], self.B[n-2], self.A[n-2]))
        op.append(cirq.CNOT(self.A[n-1],self.Z))
        op.append(cirq.TOFFOLI(self.A[n-2], self.B[n-1], self.Z))

        op.append(cirq.X(self.B[i]) for i in range(1,n-1))
        op.append(cirq.CNOT(self.C,self.B[1]))
        op.append(cirq.CNOT(self.A[i-1],self.B[i]) for i in range(2,n))
        op.append(cirq.TOFFOLI(self.A[n-3], self.B[n-2], self.A[n-2]))

        for i in range(n-3,1,-1):
            op.append(cirq.TOFFOLI(self.A[i-1], self.B[i], self.A[i]))
            op.append(cirq.CNOT(self.A[i+2],self.A[i+1]))
            op.append(cirq.X(self.B[i+1]))
        op.append(cirq.TOFFOLI(self.C,self.B[1],self.A[1]))
        op.append(cirq.CNOT(self.A[3], self.A[2]))
        op.append(cirq.X(self.B[2]))
        op.append(cirq.TOFFOLI(self.A[0], self.B[0], self.C))
        op.append(cirq.CNOT(self.A[2], self.A[1]))
        op.append(cirq.X(self.B[1]))
        op.append(cirq.CNOT(self.A[1], self.C))

        op.append(cirq.CNOT(self.A[i],self.B[i]) for i in range(n))

        circuit = cirq.Circuit()
        circuit.append(op)

        # measure
        result = []
        for k in self.B:
            result.append(k)
        result.append(self.Z)

        return circuit, result

    '''
    def construct_circuit_2cnot(self):
        n = len(self.A)
        op = []

        for i in range(n):
            qubit_c = self.A[i-1]
            if i==0:
                qubit_c = self.C
            qubit_b = self.B[i]
            qubit_a = self.A[i]

            op += self.MAJ_gate(qubit_a,qubit_b,qubit_c)

        op.append(cirq.CNOT(self.A[n-1],self.Z))

        for i in range(n-1,-1,-1):
            qubit_c = self.A[i-1]
            if i==0:
                qubit_c = self.C
            qubit_b = self.B[i]
            qubit_a = self.A[i]

            op += self.UMA_2cnot_gate(qubit_a,qubit_b,qubit_c)

        circuit = cirq.Circuit()
        circuit.append(op)

        # measure
        result = []
        for k in self.B:
            result.append(k)
        result.append(self.Z)

        return circuit, result
    '''