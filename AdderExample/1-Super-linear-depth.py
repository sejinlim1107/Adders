#Binary Adder Circuits of Asymptotically Minimum Depth, Linear Size, and Fan-Out Two
#design a similar Quantum adder

#输入A、B两个位n-bits数
import cirq
import mathematics
from mathematics import Main_task1_superlinearAdder
from utils.counting_utils import *
from qramcircuits.toffoli_decomposition import *

def main():
    #思路相同，构建电路+分解（但是论文没有说明分解方法！！！）
    #决定n位加法器
    nr_qubits = input("请输入一个整数：")
    # python中input函数输出的是一个字符串，而只有通过int进行强制转换
    nr_qubits = int(nr_qubits)

    #构造电路！！！！！！
    c=Main_task1_superlinearAdder(nr_qubits).construct_circuit(nr_qubits)#cirq circuit
    c1=Main_task1_superlinearAdder(nr_qubits)#superlinearAdder adder object

    #电路情况
    print(c1)#电路图

if __name__ == "__main__":
    main()

