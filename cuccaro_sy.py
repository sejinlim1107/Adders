"""
Implementation of the carry ripple adder in the form presented by Cuccaro
in https://arxiv.org/pdf/quant-ph/0410184.pdf
"""

import cirq
from mathematics.recycled_gate import RecycledGate

class Adder:

    # 옵션 2가지. 2cnot / 3cnot

    def __init__(self, a, b, use_dual_ancilla = False, UMA_2_CNots=True):
        #print("Carry Ripple Adder")
        self.qubits_a, self.qubits_b = a, b
        self.nr_qubits = len(self.qubits_a)
        self.use_dual_ancilla = use_dual_ancilla
        self.circuit = None

        self.qubit_c = cirq.NamedQubit("c0")
        self.qubit_z = cirq.NamedQubit("z0")
        #self.qubits_d = [cirq.NamedQubit("d" + str(i)) for i in range(self.nr_qubits)]

        '''
        self._qubit_order.append(self.qubit_c)
        for i in range(self.nr_qubits):
            self._qubit_order.append(self.qubits_b[i])
            self._qubit_order.append(self.qubits_a[i])

            if self.use_dual_ancilla:
                if i != self.nr_qubits - 1:
                    self._qubit_order.append(self.qubits_d[i])
        self._qubit_order.append(self.qubit_z)
        '''

        if UMA_2_CNots:
            self.result = self.construct_circuit_2cnot()
        else:
            self.result = self.construct_circuit_3cnot()

    def MAJ_gate(self, qubit_1, qubit_2, qubit_3):

        self.circuit.append(cirq.CNOT.on(qubit_3, qubit_1),
                            strategy = cirq.InsertStrategy.NEW)

        self.circuit.append(cirq.CNOT.on(qubit_3, qubit_2),
                            strategy = cirq.InsertStrategy.NEW)

        self.circuit.append(cirq.TOFFOLI.on(qubit_1, qubit_2, qubit_3),
                            strategy = cirq.InsertStrategy.NEW)

    def UMA_2cnot_gate(self, qubit_1, qubit_2, qubit_3):

        self.circuit.append(cirq.TOFFOLI.on(qubit_1, qubit_2, qubit_3),
                            strategy = cirq.InsertStrategy.NEW)

        self.circuit.append(cirq.CNOT.on(qubit_3, qubit_1),
                            strategy = cirq.InsertStrategy.NEW)

        self.circuit.append(cirq.CNOT.on(qubit_1, qubit_2),
                            strategy = cirq.InsertStrategy.NEW)

    def UMA_3cnot_gate(self, qubit_1, qubit_2, qubit_3):

        self.circuit.append(cirq.X.on(qubit_2),
                            strategy = cirq.InsertStrategy.NEW)

        self.circuit.append(cirq.CNOT.on(qubit_1, qubit_2),
                            strategy = cirq.InsertStrategy.NEW)

        self.circuit.append(cirq.TOFFOLI.on(qubit_1, qubit_2, qubit_3),
                            strategy = cirq.InsertStrategy.NEW)

        self.circuit.append(cirq.X.on(qubit_2),
                            strategy = cirq.InsertStrategy.NEW)

        self.circuit.append(cirq.CNOT.on(qubit_3, qubit_2),
                            strategy = cirq.InsertStrategy.NEW)

        self.circuit.append(cirq.CNOT.on(qubit_3, qubit_1),
                            strategy = cirq.InsertStrategy.NEW)


    def construct_circuit_3cnot(self):
        self.circuit = cirq.Circuit()

        """
            Propagate the carry ripple
        """

        for i in range(self.nr_qubits):
            qubit_1 = self.qubit_c
            if i > 0:
                qubit_1 = self.qubits_a[i-1]
            qubit_2 = self.qubits_b[i]
            qubit_3 = self.qubits_a[i]

            self.MAJ_gate(qubit_1, qubit_2, qubit_3)

        self.circuit.append(cirq.CNOT(self.qubits_a[self.nr_qubits - 1],
                                          self.qubit_z))

        for i in range(self.nr_qubits - 1, -1, -1):
            qubit_1 = self.qubit_c
            if i > 0:
                qubit_1 = self.qubits_a[i-1]
            qubit_2 = self.qubits_b[i]
            qubit_3 = self.qubits_a[i]

            self.UMA_3cnot_gate(qubit_1, qubit_2, qubit_3)

        # measure
        result = []
        for k in self.qubits_b:
            result.append(k)
        result.append(self.qubit_z)

        return result


    def construct_circuit_2cnot(self):
        self.circuit = cirq.Circuit()

        """
            Propagate the carry ripple
        """

        for i in range(self.nr_qubits):
            qubit_1 = self.qubit_c
            if i > 0:
                qubit_1 = self.qubits_a[i-1]
            qubit_2 = self.qubits_b[i]
            qubit_3 = self.qubits_a[i]

            self.MAJ_gate(qubit_1, qubit_2, qubit_3)

        self.circuit.append(cirq.CNOT(self.qubits_a[self.nr_qubits - 1],
                                          self.qubit_z))

        for i in range(self.nr_qubits - 1, -1, -1):
            qubit_1 = self.qubit_c
            if i > 0:
                qubit_1 = self.qubits_a[i-1]
            qubit_2 = self.qubits_b[i]
            qubit_3 = self.qubits_a[i]

            self.UMA_2cnot_gate(qubit_1, qubit_2, qubit_3)

        # measure
        result = []
        for k in self.qubits_b:
            result.append(k)
        result.append(self.qubit_z)

        return result