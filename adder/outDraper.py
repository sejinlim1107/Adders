# TODO: Document the code !!
"""
  Implementation of the carry lookahead adder
  arxiv preprint 0406142
  A logarithmic-depth quantum carry-lookahead adder
"""
import cirq
from math import floor, log2

class Adder:
    # out of place
    def __init__(self, A, B):
        """
          params: A: quantum register holding the first integer operand
          params: B: quantum register holding the second integer operand
        """
        self.A, self.B = A, B
        self.Z = [cirq.NamedQubit("Z" + str(i)) for i in range(len(self.A) + 1)]
        # n+1 크기의 결과 저장소 Z 생성
        self.circuit, self.result = self.construct_circuit()

    def w(self, n):
        return n - sum(int(floor(n / (pow(2, i)))) for i in range(1, int(log2(n)) + 1))

    def l(self, n, t):
        return int(floor(n / (pow(2, t))))

    def construct_circuit(self):
        n = len(self.A)
        init = []
        p_round = []
        g_round = []
        c_round = []
        p_round_uncom = []


        length = n - self.w(n) - floor(log2(n))
        ancilla = [cirq.NamedQubit("a" + str(i)) for i in range(length)]  # 논문에서 X라 지칭

        # Init round
        for i in range(n):
            init.append(cirq.TOFFOLI(self.A[i], self.B[i], self.Z[i + 1]))

        for i in range(1,n):
            init.append(cirq.CNOT(self.A[i], self.B[i]))

        # P-round
        #print("P-round")
        idx = 0  # ancilla idx
        tmp = 0 # m=1일 때 idx 저장해두기
        for t in range(1, int(log2(n))):
            pre = tmp  # (t-1)일 때의 첫번째 자리 저장
            for m in range(1, self.l(n, t)):
                if t == 1: # B에 저장되어있는 애들로만 연산 가능
                    # print(2*m,2*m+1,idx)
                    p_round.append(cirq.TOFFOLI(self.B[2*m], self.B[2*m+1], ancilla[idx]))
                else: # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                    # print(pre - 1 + 2 * m,pre - 1 + 2 * m + 1,idx)
                    p_round.append(cirq.TOFFOLI(ancilla[pre-1+2*m], ancilla[pre-1+2*m+1], ancilla[idx]))
                if m==1:
                    tmp = idx
                idx += 1


        # G-round
        #print("G-round")
        pre = 0  # The number of cumulative p(t-1)
        idx = 0  # ancilla idx
        for t in range(1, int(log2(n))+1):
            for m in range(self.l(n, t)):
                if t == 1: # B에 저장되어있는 애들로만 연산 가능
                    # print(int(pow(2, t) * m + pow(2, t - 1)), 2*m+1, int(pow(2, t) * (m + 1)))
                    g_round.append(cirq.TOFFOLI(self.Z[int(pow(2, t)*m + pow(2, t-1))], self.B[2 * m + 1], self.Z[int(pow(2, t)*(m+1))]))
                else: # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                    #print(int(pow(2, t) * m + pow(2, t - 1)), idx+2*m, int(pow(2, t) * (m + 1)))
                    g_round.append(cirq.TOFFOLI(self.Z[int(pow(2, t)*m + pow(2, t-1))], ancilla[idx+2*m], self.Z[int(pow(2, t)*(m+1))]))
            if t != 1:
                pre = pre + self.l(n, t - 1) - 1
                idx = pre

        # C-round
        #print("C-round")
        if int(log2(n)) - 1 == int(log2(2 * n / 3)):  # p(t-1)까지 접근함
            iter = self.l(n, int(log2(n)) - 1) - 1  # 마지막 pt의 개수
        else:  # p(t)까지 접근함
            iter = 0
        pre = 0  # (t-1)일 때의 첫번째 idx
        for t in range(int(log2(2*n/3)),0,-1):
            for m in range(1,self.l((n-pow(2,t-1)), t)+1):
                if t == 1:  # B에 저장되어있는 애들로만 연산 가능
                    # print(int(pow(2, t) * m), 2*m, int(pow(2, t) * m + pow(2, t - 1)))
                    c_round.append(
                        cirq.TOFFOLI(self.Z[int(pow(2, t) * m)], self.B[2 * m], self.Z[int(pow(2, t) * m + pow(2, t - 1))]))
                else:
                    if m == 1:
                        iter += self.l(n, t - 1) - 1
                        pre = length - 1 - iter
                    # print(int(pow(2, t) * m),pre + 2 * m,int(pow(2, t) * m + pow(2, t-1)))
                    c_round.append(cirq.TOFFOLI(self.Z[int(pow(2, t) * m)], ancilla[pre + 2 * m],self.Z[int(pow(2, t) * m + pow(2, t - 1))]))

        # P-inverse round
        # print("P-inv-rounds")
        pre = 0  # (t-1)일 때의 첫번째 idx
        iter = self.l(n, int(log2(n)) - 1) - 1  # 마지막 pt의 개수
        iter2 = 0  # for idx
        idx = 0
        for t in reversed(range(1, int(log2(n)))):
            for m in range(1, self.l(n, t)):
                if t == 1:  # B에 저장되어있는 애들로만 연산 가능
                    # print(2*m,2*m+1,m-t)
                    p_round_uncom.append(cirq.TOFFOLI(self.B[2 * m], self.B[2 * m + 1], ancilla[m - t]))
                else:  # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                    if m == 1:
                        iter += self.l(n, t - 1) - 1  # p(t-1) last idx
                        pre = length - iter
                        iter2 += (self.l(n, t) - 1)
                        idx = length - iter2
                    # print(pre - 1 + 2 * m,pre - 1 + 2 * m + 1,idx-1+m)
                    p_round_uncom.append(cirq.TOFFOLI(ancilla[pre - 1 + 2 * m], ancilla[pre - 1 + 2 * m + 1], ancilla[idx - 1 + m]))


        # Last round
        last_round = [cirq.CNOT(self.B[i], self.Z[i]) for i in range(n)]
        last_round += [cirq.CNOT(self.A[0], self.Z[0])]
        last_round += [cirq.CNOT(self.A[i], self.B[i]) for i in range(1, n)]

        circuit = cirq.Circuit()

        # Init
        circuit += init

        # P-round
        circuit += p_round

        # G-round
        circuit += g_round

        # C-round
        circuit += c_round

        # P-inverse
        circuit += p_round_uncom

        # Last round
        circuit += last_round

        result = []

        for k in self.Z:
            result.append(k)

        return circuit, result
