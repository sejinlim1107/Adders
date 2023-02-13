#输入n,构建n位Cucarro Adder
#输出电路图 + 4个指标
import cirq
import numpy as np
import mathematics
from mathematics import CarryRipple8TAdder
from utils.counting_utils import *
from qramcircuits.toffoli_decomposition import *

def main():
    #思路相同，构建电路+分解（但是论文没有说明分解方法！！！）

    #决定n位加法器
    #nr_qubits = input("请输入一个整数：")
    # python中input函数输出的是一个字符串，而只有通过int进行强制转换
    #nr_qubits = int(nr_qubits)

    circuit = cirq.Circuit()
    #a = [cirq.NamedQubit("a" + str(i)) for i in range(3)]
    #b = [cirq.NamedQubit("b" + str(i)) for i in range(3)]


    #circuit.append(cirq.X(a[0]))
    circuit.append(CarryRipple8TAdder(3).circuit)
    print(circuit)
    '''
    #构造电路
    c=CarryRipple8TAdder(nr_qubits, use_dual_ancilla = False).construct_circuit_3cnot(nr_qubits)
    qubit_order=CarryRipple8TAdder(nr_qubits, use_dual_ancilla = False,UMA_2_CNots=False).qubit_order
    c1=CarryRipple8TAdder(nr_qubits, use_dual_ancilla = False)

    #电路情况
    print(c1)#电路图

    #Decomposition: 暂定使用A0T2
    ct=cirq.Circuit(ToffoliDecomposition.construct_decomposed_moments(c.moments, ToffoliDecompType.ZERO_ANCILLA_TDEPTH_2_COMPUTE))
    print(ct)
   #T-count、T-depth、Qubit-count、CNOT-count
    print("分解前电路")
    print("T-depth= ", count_t_depth_of_circuit(c))
    print("T-count= ", count_t_of_circuit(c))
    print("CNOT-count= ", count_cnot_of_circuit(c))
    print("Qubit-count=",len(c.all_qubits()))
    print("Toffoli-count=", count_toffoli_of_circuit(c))

    print("分解后电路")
    print("Qubit-count=", len(ct.all_qubits()))  # 2n+2
    print("T-depth= ", count_t_depth_of_circuit(ct)) # 4n
    print("T-count= ", count_t_of_circuit(ct)) # 8n
    '''

    '''
    aaa = "1100"
    bbb = "1100"

    initial_state = str(0)
    for i in range(nr_qubits):
        initial_state = initial_state + aaa[i] + bbb[i]
    initial_state = initial_state + str(0)

    initial_state = [int(initial_state[i], 2) for i in range(2 * nr_qubits + 2)] #number of qubits
    print('check')
    print(initial_state)
    # simulator
    simulator = cirq.Simulator()
    result1 = simulator.simulate(c, qubit_order=qubit_order, initial_state=initial_state)
    result = str(result1)
    print("result1", result1)
    result = result[result.index('|') + 1:-1]

    print("result", result)
    real_result =""
    real_result = result[5]
    real_result = real_result + result[6]
    real_result = real_result + result[7]
    real_result = real_result + result[8]
    real_result = real_result + result[9]
    #real_result + real_result[nr_qubits+1]


    print("result", real_result)
    '''


if __name__ == "__main__":
     main()
