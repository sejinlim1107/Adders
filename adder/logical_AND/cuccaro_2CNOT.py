"""
Implementation of the carry ripple adder in the form presented by Cuccaro
in https://arxiv.org/pdf/quant-ph/0410184.pdf
"""

import cirq
from mathematics.recycled_gate import RecycledGate

#Circuit return 안하게 수정했음 (circuit 여러번 호출하면 addertest에서 병렬처리가 안됨)

class Adder:

    # 옵션 2가지. 2cnot / 3cnot

    def __init__(self, a, b):
        #print("Carry Ripple Adder")
        self.A, self.B = a, b
        self.nr_qubits = len(self.A)
        self.C = cirq.NamedQubit("c0")
        self.Z = cirq.NamedQubit("z0")

        self.circuit, self.result = self.construct_circuit_2cnot()

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

        # circuit = cirq.Circuit()
        # circuit.append(op)

        # measure
        result = []
        for k in self.B:
            result.append(k)
        result.append(self.Z)

        return op, result