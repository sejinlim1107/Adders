# TODO: Document the code !!
"""
  Implementation of the carry lookahead adder
  arxiv preprint 0406142
  A logarithmic-depth quantum carry-lookahead adder
"""
import cirq
import math as mt


class Adder:
    # in-place
    def __init__(self, A, B):
        """
          params: A: quantum register holding the first integer operand
          params: B: quantum register holding the second integer operand
        """
        self.A, self.B = A, B
        self.circuit, self.result = self.construct_circuit()

    def w(self, n):
        return n - sum(int(mt.floor(n / (mt.pow(2, i)))) for i in range(1, int(mt.log2(n)) + 1))

    def l(self, n, t):
        return int(mt.floor(n / (mt.pow(2, t))))

    def construct_rounds(self):
        n = len(self.A)
        init = []
        p_round = []
        g_round = []
        c_round = []
        p_round_uncomp = []
        g_round_uncomp = []
        c_round_uncomp = []

        length = n - self.w(n) - mt.floor(mt.log2(n))
        ancilla1 = [cirq.NamedQubit("z" + str(i)) for i in range(n)]  # z[1] ~ z[n] 저장
        ancilla2 = [cirq.NamedQubit("a" + str(i)) for i in range(length)] # 논문에서 X라고 지칭되는 ancilla

        # Init round
        for i in range(n):
            init.append(cirq.TOFFOLI(self.A[i], self.B[i], ancilla1[i])) # ancilla1[0] == Z[1]
            print("1번")
            print(i)
        for i in range(n):
            init.append(cirq.CNOT(self.A[i], self.B[i]))
            print("2번")
            print(i)

        # P-round
        # First moment
        idx = 0  # ancilla idx
        pre = 0 # 이전 t-1일 때의 [1]의 상대적 위치.
        tmp = 0 # (n-1) adder일 때 배열 끊는 기준
        for t in range(1, int(mt.log2(n))):
            for m in range(1, self.l(n, t)):
                if t == 1: # B에 저장되어있는 애들로만 연산 가능
                    p_round.append(cirq.TOFFOLI(self.B[2*m], self.B[2*m+1], ancilla2[idx]))
                    print("P라운드 t, m")
                    print(t,m)
                else: # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                    p_round.append(cirq.TOFFOLI(ancilla2[pre-1+2*m], ancilla2[pre-1+2*m+1], ancilla2[idx]))
                    print(t,m)
                    # p_round.append(cirq.TOFFOLI(ancilla[idx-self.l(n,t-1)+2*m], ancilla[idx-self.l(n,t-1)+2*m+1], ancilla[idx]))
                    # 이건 절대적 위치 계산한 식임. 이것도 제대로 동작하긴 함.
                if m == 1: # 여기 위치가 맞음. t==1일 때 이 if문을 통과하면서 저장할 것임. (t-1) for문의 m=1을 저장하는게 목표.
                    pre = idx
                idx += 1

            # uncomp part
            if self.l(n, t) == self.l(n - 1, t):
                p_round_uncomp += p_round[tmp:]
                tmp = len(p_round)
            else:
                p_round_uncomp += p_round[tmp:-1]
                tmp = len(p_round)

        if n!=1 and int(mt.log2(n)) != int(mt.log2(n-1)):
            p_round_uncomp = p_round_uncomp[:-(self.l(n, int(mt.log2(n))-1)-1)] # 잘못 추가된거 삭제

        # G-round
        # First moment
        pre = 0
        tmp = 0
        for t in range(1, int(mt.log2(n))+1):
            for m in range(self.l(n, t)):
                if t == 1: # B에 저장되어있는 애들로만 연산 가능
                    #print(int(mt.pow(2, t)*m + mt.pow(2, t-1)-1),2 * m + 1,int(mt.pow(2, t)*(m+1))-1)
                    g_round.append(cirq.TOFFOLI(ancilla1[int(mt.pow(2, t)*m + mt.pow(2, t-1))-1], self.B[2 * m + 1], ancilla1[int(mt.pow(2, t)*(m+1))-1]))
                    print("G라운드 t, m")
                    print(t, m)
                else: # t가 1보다 클 때는 ancilla에 저장된 애들도 이용해야함
                    idx = pre-1+2*m+1
                    #print(int(mt.pow(2, t)*m + mt.pow(2, t-1))-1,idx,int(mt.pow(2, t)*(m+1))-1)
                    g_round.append(cirq.TOFFOLI(ancilla1[int(mt.pow(2, t)*m + mt.pow(2, t-1))-1], ancilla2[idx], ancilla1[int(mt.pow(2, t)*(m+1))-1]))
                    print(t, m)
            if t > 1:
                pre = idx+1

            # uncomp part
            if self.l(n, t) == self.l(n - 1, t):
                g_round_uncomp += g_round[tmp:]
                tmp = len(g_round)
            else:
                g_round_uncomp += g_round[tmp:-1]
                tmp = len(g_round)

        if n!=1 and int(mt.log2(n)) != int(mt.log2(n - 1)):
            g_round_uncomp = g_round_uncomp[:-(self.l(n, int(mt.log2(n))) - 1)]  # 잘못 추가된거 삭제

        # C-round
        # First moment of C-round
        # 이거 순서대로 담고 마지막에 뒤집어도 될 듯
        tmp = 0
        for t in range(int(mt.log2(2*n/3)),0,-1):
            for m in range(1,self.l((n-pow(2,t-1)), t)+1):
                if t == 1:  # B에 저장되어있는 애들로만 연산 가능
                    c_round.append(
                        cirq.TOFFOLI(ancilla1[int(mt.pow(2, t) * m)-1], self.B[2 * m], ancilla1[int(mt.pow(2, t) * m + mt.pow(2, t - 1))-1]))
                else:
                    #print(int(mt.pow(2, t) * m)-1,len(ancilla2)-1-self.l(n,t)-1+2*m,int(mt.pow(2, t) * m + mt.pow(2, t - 1))-1)
                    c_round.append(cirq.TOFFOLI(ancilla1[int(mt.pow(2, t) * m)-1], ancilla2[len(ancilla2)-2-self.l(n,t)-1+2*m],ancilla1[int(mt.pow(2, t) * m + mt.pow(2, t - 1))-1]))

            # uncomp part
            if self.l((n-pow(2,t-1)), t) == self.l(((n-1)-pow(2,t-1)), t):
                c_round_uncomp += c_round[tmp:]
                tmp = len(c_round)
            else:
                c_round_uncomp += c_round[tmp:-1]
                tmp = len(c_round)

        t = int(mt.log2(2*n/3))
        if n!=1 and int(mt.log2(2*n/3)) != int(mt.log2(2*(n-1)/3)):
            c_round_uncomp = c_round_uncomp[:self.l((n-pow(2,t-1)), t)-1]+c_round_uncomp[self.l((n-pow(2,t-1)), t):] # 잘못 추가된거 삭제

        # Last round
        last_round = [cirq.CNOT(ancilla1[i-1], self.B[i]) for i in range(1, n)]
        last_round += [cirq.X(self.B[i]) for i in range(n-1)]
        last_round += [cirq.CNOT(self.A[i], self.B[i]) for i in range(1, n-1)]

        return init, p_round, g_round, c_round, last_round, p_round_uncomp, g_round_uncomp, c_round_uncomp, ancilla1

    def construct_circuit(self):
        """
          returns the CLA circuit
        """

        """
          Computation part of the circuit
        """
        init_comp, p_round_comp, g_round_comp, c_round_comp, last_round, p_round_uncomp, g_round_uncomp, c_round_uncomp, ancilla = self.construct_rounds()
        # Init
        circuit = cirq.Circuit(init_comp)

        # P-round
        circuit += cirq.Circuit(p_round_comp)

        # G-round
        circuit += cirq.Circuit(g_round_comp)

        # C-round
        circuit += cirq.Circuit(c_round_comp)

        # P-inverse
        circuit += cirq.Circuit(p_round_comp[::-1])

        # Last round
        circuit += cirq.Circuit(last_round)

        ### Step7. Section3 in reverse. (n-1)bit adder ###
        n = len(self.A)

        circuit += cirq.Circuit(p_round_uncomp)
        circuit += cirq.Circuit(c_round_uncomp[::-1])
        circuit += cirq.Circuit(g_round_uncomp[::-1])
        circuit += cirq.Circuit(p_round_uncomp[::-1])

        '''
        ### Step7. Section3 in reverse. (n-1)bit adder ###

        p_round_uncomp = 0
        # P round에서 어디까지 잘라야하는지 계산. 방식을 개선시킬 수 있을 것 같지만 일단 보류.
        start = 0
        end = 0
        for t in range(1, int(mt.log2(n - 1))):
            for m in range(1, int(mt.floor((n - 1) / (mt.pow(2, t))))):
                end += 1
            p_round_uncomp += p_round_comp[start:end+1] # 기존 P-round 자르기
            start = int(mt.floor((n) / (mt.pow(2, t))))-1

        #print(cnt)

        p_round_uncomp = p_round_comp[:cnt] # 기존 P-round 자르기
        circuit += cirq.Circuit(p_round_uncomp)

        # C
        cnt = 0
        for t in range(int(mt.log2(2*(n-1)/3)),0,-1):
            for m in range(1,self.l(((n-1)-pow(2,t-1)), t)+1):
                cnt += 1


        c_round_uncomp = c_round_comp[:cnt][::-1] # 기존 C-round 자르기 -> 뒤집기
        circuit += cirq.Circuit(c_round_uncomp)

        # G
        cnt = 0
        for t in range(1, int(mt.log2(n-1)) + 1):
            for m in range(self.l(n-1, t)):
                cnt += 1

        g_round_uncomp = g_round_comp[:cnt][::-1]
        circuit += cirq.Circuit(g_round_uncomp)

        # P^(-1)
        circuit += cirq.Circuit(p_round_uncomp[::-1])
        
        '''

        fin = [cirq.CNOT(self.A[i], self.B[i]) for i in range(1,n-1)]
        fin += [cirq.TOFFOLI(self.A[i], self.B[i], ancilla[i]) for i in range(n - 1)]
        fin += [cirq.X(self.B[i]) for i in range(n - 1)]

        circuit.append(fin)

        result = []

        for k in self.B:
            result.append(k)
        result.append(ancilla[-1])

        # print(circuit)
        return circuit, result
