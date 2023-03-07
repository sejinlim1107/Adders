"""
Implementation of the carry ripple adder in the form presented by Cuccaro
in https://arxiv.org/pdf/quant-ph/0410184.pdf
"""

import cirq
from mathematics.recycled_gate import RecycledGate

class Adder:

    # 옵션 2가지. 2cnot / 3cnot

    def __init__(self, a, b, UMA_2_CNots=False):
        #print("Carry Ripple Adder")
        self.A, self.B = a, b
        self.nr_qubits = len(self.A)
        self.circuit = None
        self.C = cirq.NamedQubit("c0")
        self.Z = cirq.NamedQubit("z0")

        if self.nr_qubits == 1:
            self.result = self.construct_circuit1()
        else:
            if UMA_2_CNots:
                self.result = self.construct_circuit_2cnot()
            else:
                self.result = self.construct_circuit_3cnot()

    def construct_circuit1(self):
        self.circuit = cirq.Circuit()
        self.circuit.append(cirq.TOFFOLI(self.B[0],self.A[0],self.Z))
        self.circuit.append(cirq.CNOT(self.A[0],self.B[0]))

    def MAJ_gate(self, a, b, c):

        self.circuit.append(cirq.CNOT.on(a, b))
        self.circuit.append(cirq.CNOT.on(a, c))
        self.circuit.append(cirq.TOFFOLI.on(c, b, a))

    def UMA_2cnot_gate(self, a, b, c):

        self.circuit.append(cirq.TOFFOLI.on(c, b, a))
        self.circuit.append(cirq.CNOT.on(a, c))
        self.circuit.append(cirq.CNOT.on(c, b))

    def UMA_3cnot_gate(self, a, b, c):

        self.circuit.append(cirq.X.on(b))
        self.circuit.append(cirq.CNOT.on(c, b))
        self.circuit.append(cirq.TOFFOLI.on(c, b, a))
        self.circuit.append(cirq.X.on(b))
        self.circuit.append(cirq.CNOT.on(a, c))
        self.circuit.append(cirq.CNOT.on(a, b))

    def construct_circuit_3cnot(self):
        self.circuit = cirq.Circuit()

        for i in range(self.nr_qubits):


        """
            Propagate the carry ripple
        """

        for i in range(self.nr_qubits):
            qubit_1 = self.C
            if i > 0:
                qubit_1 = self.A[i - 1]
            qubit_2 = self.B[i]
            qubit_3 = self.A[i]

            self.MAJ_gate(qubit_1, qubit_2, qubit_3)

        self.circuit.append(cirq.CNOT(self.A[self.nr_qubits - 1],
                                      self.Z))

        for i in range(self.nr_qubits - 1, -1, -1):
            qubit_1 = self.C
            if i > 0:
                qubit_1 = self.A[i - 1]
            qubit_2 = self.B[i]
            qubit_3 = self.A[i]

            self.UMA_3cnot_gate(qubit_1, qubit_2, qubit_3)

        # measure
        result = []
        for k in self.B:
            result.append(k)
        result.append(self.Z)

        return result


    def construct_circuit_2cnot(self):
        self.circuit = cirq.Circuit()

        """
            Propagate the carry ripple
        """

        for i in range(self.nr_qubits):
            qubit_1 = self.C
            if i > 0:
                qubit_1 = self.A[i - 1]
            qubit_2 = self.B[i]
            qubit_3 = self.A[i]

            self.MAJ_gate(qubit_1, qubit_2, qubit_3)

        self.circuit.append(cirq.CNOT(self.A[self.nr_qubits - 1],
                                      self.Z))

        for i in range(self.nr_qubits - 1, -1, -1):
            qubit_1 = self.C
            if i > 0:
                qubit_1 = self.A[i - 1]
            qubit_2 = self.B[i]
            qubit_3 = self.A[i]

            self.UMA_2cnot_gate(qubit_1, qubit_2, qubit_3)

        # measure
        result = []
        for k in self.B:
            result.append(k)
        result.append(self.Z)

        return result