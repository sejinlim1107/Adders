"""
    Implementation of control adder from : arXiv:0910.2530, 2009
"""
import cirq


class Adder:
    # type에 따라서 combination_Method랑 RCA 두가지 버전이 있음

    def __init__(self, A, B, ancillae=None, type = True):
        #self._qubit_order = []
        self.A = A
        self.B = B
        self.nr_qubits = len(A)
        self.type = type

        if ancillae != None:#Ancillae
            self.ancillae = ancillae
        else:
            self.ancillae = cirq.NamedQubit("ancilla1")

        self.circuit, self.result = self.construct_circuit()

        '''
        for i in range(self.nr_qubits):
            self.circuit.append(self.B[i])
            self.circuit.append(self.A[i])
        self.circuit.append(self.ancillae)
        '''

    def construct_circuit(self):
        # The set of CNOTs between Ai and Bi
        firs_set_of_CNOTs=[cirq.Moment([cirq.CNOT(self.A[i], self.B[i]) for i in range(1, self.nr_qubits)])]

        # The set of CNOTs between Ai and Ai+1
        second_set_of_CNOTs=[]

        # The set of CNOTs between Ai, Bi and Ai+1
        firs_set_of_toff=[cirq.Moment([cirq.TOFFOLI(self.B[0], self.A[0], self.A[1])])]

        last_set_of_toff=[cirq.Moment([cirq.CNOT(self.A[0], self.B[0])])]

        single=[]
        for i in range(1, self.nr_qubits-1):
            # Constructing the first part of the circuit
            second_set_of_CNOTs.append(cirq.Moment([cirq.CNOT(self.A[i], self.A[i+1])]))
            firs_set_of_toff.append(cirq.Moment([cirq.TOFFOLI(self.B[i], self.A[i], self.A[i+1])]))

            # Constructing the last part of the circuit
            last_set_of_toff.append(cirq.Moment([cirq.CNOT(self.A[i], self.B[i])]))
        last_set_of_toff.append(cirq.Moment([cirq.CNOT(self.A[-1], self.B[-1])]))

        # Adding or removing the N+1st qubit depending on choice
        if self.type:
            firs_set_of_toff.append(cirq.Moment([cirq.TOFFOLI(self.B[-1], self.A[-1], self.ancillae)])) # here
            single = [cirq.Moment([cirq.CNOT(self.A[-1], self.ancillae)])]

        circuit = cirq.Circuit()
        # Constrcting the fist half of the circuit
        circuit.append(firs_set_of_CNOTs, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        circuit.append(single, strategy=cirq.InsertStrategy.NEW_THEN_INLINE) # here
        circuit.append(second_set_of_CNOTs[::-1], strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        circuit.append(firs_set_of_toff, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)

        # Balancing the circuit
        if self.type:
            firs_set_of_toff = firs_set_of_toff[::-1][1:]
        else:
            firs_set_of_toff = firs_set_of_toff[::-1]

        # Constructing the last part of the circuit
        last_set_of_toff = last_set_of_toff[::-1]
        for i in range(len(firs_set_of_toff)):
            circuit.append(last_set_of_toff[i], strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
            circuit.append(firs_set_of_toff[i], strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        circuit.append(last_set_of_toff[-1], strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        circuit.append(second_set_of_CNOTs, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        circuit.append(firs_set_of_CNOTs, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)

        # measure
        result = []
        for k in self.B:
            result.append(k)
        result.append(self.ancillae) # if ancillae != None <-- 이 값에 따라 ancillae가 달라짐
                                     # 일단 예제에서 다 None으로 설정되어있음

        return circuit, result