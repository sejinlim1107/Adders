"""
    Implementation of control adder from : arXiv:0910.2530, 2009
"""
import cirq

#Circuit return 안하게 수정했음 (circuit 여러번 호출하면 addertest에서 병렬처리가 안됨)

class Adder:
    # type에 따라서 combination_Method랑 RCA 두가지 버전이 있음

    def __init__(self, A, B, ancillae=None, type = True):
        self.A = A
        self.B = B
        self.nr_qubits = len(A)
        self.type = type

        if ancillae != None:#Ancillae
            self.ancillae = ancillae
        else:
            self.ancillae = cirq.NamedQubit("ancilla1")

        if self.nr_qubits > 1:
            self.circuit, self.result = self.construct_circuit()
        else: # 1비트 덧셈
            self.circuit, self.result = self.construct_circuit1()

    def construct_circuit1(self):
        op = []

        op.append(cirq.TOFFOLI(self.A[0], self.B[0], self.ancillae))
        op.append(cirq.CNOT(self.A[0], self.B[0]))

        #circuit = cirq.Circuit()
        #circuit.append(op)

        result = []
        for k in self.B:
            result.append(k)
        result.append(self.ancillae)

        return op, result

    def construct_circuit(self):
        n = len(self.A)
        
        # The set of CNOTs between Ai and Bi
        firs_set_of_CNOTs=[cirq.CNOT(self.A[i], self.B[i]) for i in range(1, n)]

        # The set of CNOTs between Ai and Ai+1
        second_set_of_CNOTs=[]

        # The set of CNOTs between Ai, Bi and Ai+1
        firs_set_of_toff=[cirq.TOFFOLI(self.B[0], self.A[0], self.A[1])]

        last_set_of_CNOTs=[cirq.CNOT(self.A[0], self.B[0])]

        single=[]
        for i in range(1, n-1):
            # Constructing the first part of the circuit
            second_set_of_CNOTs.append(cirq.CNOT(self.A[i], self.A[i+1]))
            firs_set_of_toff.append(cirq.TOFFOLI(self.B[i], self.A[i], self.A[i+1]))

            # Constructing the last part of the circuit
            last_set_of_CNOTs.append(cirq.CNOT(self.A[i], self.B[i]))
        last_set_of_CNOTs.append(cirq.CNOT(self.A[-1], self.B[-1]))

        # Adding or removing the N+1st qubit depending on choice
        if self.type:
            firs_set_of_toff.append(cirq.TOFFOLI(self.B[-1], self.A[-1], self.ancillae)) # here
            single = [cirq.CNOT(self.A[-1], self.ancillae)]

        # circuit = cirq.Circuit()
        # Constrcting the fist half of the circuit
        # circuit.append(firs_set_of_CNOTs, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        # circuit.append(single, strategy=cirq.InsertStrategy.NEW_THEN_INLINE) # here
        # circuit.append(second_set_of_CNOTs[::-1], strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        # circuit.append(firs_set_of_toff, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        op = []

        op.append(firs_set_of_CNOTs)
        op.append(single)  # here
        op.append(second_set_of_CNOTs[::-1])
        op.append(firs_set_of_toff)

        # Balancing the circuit
        if self.type:
            firs_set_of_toff = firs_set_of_toff[::-1][1:]
        else:
            firs_set_of_toff = firs_set_of_toff[::-1]

        # Constructing the last part of the circuit
        last_set_of_CNOTs = last_set_of_CNOTs[::-1]
        # for i in range(len(firs_set_of_toff)):
        #     circuit.append(last_set_of_CNOTs[i], strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        #     circuit.append(firs_set_of_toff[i], strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        # circuit.append(last_set_of_CNOTs[-1], strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        # circuit.append(second_set_of_CNOTs, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        # circuit.append(firs_set_of_CNOTs, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
        for i in range(len(firs_set_of_toff)):
            op.append(last_set_of_CNOTs[i])
            op.append(firs_set_of_toff[i])
        op.append(last_set_of_CNOTs[-1])
        op.append(second_set_of_CNOTs)
        op.append(firs_set_of_CNOTs)

        # measure
        result = []
        for k in self.B:
            result.append(k)
        result.append(self.ancillae) # if ancillae != None <-- 이 값에 따라 ancillae가 달라짐
                                     # 일단 예제에서 다 None으로 설정되어있음

        return op, result