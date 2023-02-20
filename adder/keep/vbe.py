"""
VBE plain adder
https://journals.aps.org/pra/abstract/10.1103/PhysRevA.54.147

논문 링크
https://sci-hub.st/https://journals.aps.org/pra/abstract/10.1103/PhysRevA.54.147
"""

#얜 너무 오래됨. 쿠카로가 얘 최적화함. 무시

import cirq
from utils.counting_utils import count_t_depth_of_circuit, count_cnot_of_circuit, count_t_of_circuit
#from .recycled_gate import RecycledGate

class Adder():

    def __init__(self, a, b):
        #print("VBE Adder")
        self.qubits_a, self.qubits_b = a,b
        self.nr_qubits = len(self.qubits_a)
        self.circuit = None

        self.qubits_c = [cirq.NamedQubit("c" + str(i)) for i in range(self.nr_qubits)]
        self.qubits_b = [cirq.NamedQubit("B" + str(i)) for i in range(self.nr_qubits+1)]

        self.result = self.construct_circuit(self.nr_qubits)

    #control在前，not在后,L表示黑条在左边，R表示黑条在右边
    def L_CARRY_gate(self, qubit_4, qubit_3, qubit_2, qubit_1):
        self.circuit.append(cirq.TOFFOLI.on(qubit_4, qubit_2, qubit_1),
                            strategy=cirq.InsertStrategy.NEW)
        self.circuit.append(cirq.CNOT.on(qubit_3, qubit_2),
                            strategy=cirq.InsertStrategy.NEW)
        self.circuit.append(cirq.TOFFOLI.on(qubit_3, qubit_2, qubit_1),
                            strategy = cirq.InsertStrategy.NEW)


    def L_SUM_gate(self, qubit_3, qubit_2, qubit_1):
        self.circuit.append(cirq.CNOT.on(qubit_3, qubit_1),
                            strategy=cirq.InsertStrategy.NEW)
        self.circuit.append(cirq.CNOT.on(qubit_2, qubit_1),
                            strategy = cirq.InsertStrategy.NEW)


    def R_CARRY_gate(self, qubit_4, qubit_3, qubit_2, qubit_1):
        self.circuit.append(cirq.TOFFOLI.on(qubit_3, qubit_2, qubit_1),
                            strategy=cirq.InsertStrategy.NEW)
        self.circuit.append(cirq.CNOT.on(qubit_3, qubit_2),
                            strategy=cirq.InsertStrategy.NEW)
        self.circuit.append(cirq.TOFFOLI.on(qubit_4, qubit_2, qubit_1),
                            strategy=cirq.InsertStrategy.NEW)



    def R_SUM_gate(self, qubit_3, qubit_2, qubit_1):
        self.circuit.append(cirq.CNOT.on(qubit_2, qubit_1),
                            strategy=cirq.InsertStrategy.NEW)
        self.circuit.append(cirq.CNOT.on(qubit_3, qubit_1),
                            strategy=cirq.InsertStrategy.NEW)



    def construct_circuit(self, nr_qubits):
        self.circuit = cirq.Circuit()

        """
            Propagate the carry ripple
        """

        for i in range(nr_qubits):
            qubit_1 = self.qubits_c[i]
            qubit_2 = self.qubits_a[i]
            qubit_3 = self.qubits_b[i]
            if i < nr_qubits-1:
                qubit_4 = self.qubits_c[i+1]
            else:
                qubit_4 = self.qubits_b[i+1]
            self.R_CARRY_gate(qubit_1, qubit_2, qubit_3,qubit_4)

        self.circuit.append(cirq.ops.CNOT(self.qubits_a[nr_qubits - 1],
                                          self.qubits_b[nr_qubits - 1]))

        self.R_SUM_gate(self.qubits_c[nr_qubits - 1],self.qubits_a[nr_qubits - 1],self.qubits_b[nr_qubits - 1])

        for i in range(nr_qubits - 2, -1,-1):
            qubit_1 = self.qubits_c[i]
            qubit_2 = self.qubits_a[i]
            qubit_3 = self.qubits_b[i]
            qubit_4 = self.qubits_c[i+1]

            self.L_CARRY_gate(qubit_1, qubit_2, qubit_3,qubit_4)
            self.R_SUM_gate(qubit_1, qubit_2, qubit_3)

        # measure
        result = []
        for k in self.qubits_b:
            result.append(k)

        return result