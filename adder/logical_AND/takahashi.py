"""
    Implementation of control adder from : arXiv:0910.2530, 2009
"""
import cirq

#Circuit return 안하게 수정했음 (circuit 여러번 호출하면 addertest에서 병렬처리가 안됨)

class Adder:

    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.nr_qubits = len(A)
        self.type = type
        self.Z = cirq.NamedQubit("Z")

        if self.nr_qubits > 1:
            self.circuit, self.result = self.construct_circuit()
        else: # 1비트 덧셈
            self.circuit, self.result = self.construct_circuit1()

    def construct_circuit1(self):
        op = []

        op.append(cirq.TOFFOLI(self.A[0], self.B[0], self.Z))
        op.append(cirq.CNOT(self.A[0], self.B[0]))

        #circuit = cirq.Circuit()
        #circuit.append(op)

        result = []
        for k in self.B:
            result.append(k)
        result.append(self.Z)

        return op, result

    def construct_circuit(self):
        n = len(self.A)
        op = []

        op.append(cirq.CNOT(self.A[i], self.B[i]) for i in range(1, n))
        op.append(cirq.CNOT(self.A[n-1],self.Z))
        op.append(cirq.CNOT(self.A[i], self.A[i+1]) for i in range(n-2,0,-1))
        op.append(cirq.TOFFOLI(self.A[i], self.B[i], self.A[i+1]) for i in range(n-1))
        op.append(cirq.TOFFOLI(self.A[n-1], self.B[n-1], self.Z))

        for i in range(n - 1, 0, -1):
            op.append(cirq.CNOT(self.A[i], self.B[i]))
            op.append(cirq.TOFFOLI(self.B[i-1], self.A[i-1], self.A[i]))
        op.append(cirq.CNOT(self.A[i], self.A[i+1]) for i in range(1,n-1))
        op.append(cirq.CNOT(self.A[i], self.B[i]) for i in range(n))

        # measure
        result = []
        for k in self.B:
            result.append(k)
        result.append(self.Z) # if ancillae != None <-- 이 값에 따라 ancillae가 달라짐
                                     # 일단 예제에서 다 None으로 설정되어있음

        return op, result