# 64 bits quantum high radix adder
import cirq
import mathematics
import random
from AdderExample import Craig_Gidney
from AdderExample.Q_BrentKung import Q_BK
from AdderExample.Q_high_radix_layer import High_radix_layer
from AdderExample.Quantum_MUX import Q_MUX
from AdderExample.Quantum_pg import Q_pg
import math


def Quantum_High_Radix(add_bit_num,radix_num):
    CSA_bits = radix_num


    '''
    Part1：m bits caary_out Craig Gidney adder √ T-depth=m
    

    c0_Craig_Gidney,s0=Craig_Gidney.Craig_Gidney_adder(nr_qubits=CSA_bits, c0=0, aaa="1010", bbb="1010") #由低位到高位,高位为0
    print(c0_Craig_Gidney)
    print(s0)
    '''


    '''
    Part2：m bits Craig Gidney CSA adder   √ 
    
    c1_Craig_Gidney, s1 = Craig_Gidney.Craig_Gidney_adder(nr_qubits=CSA_bits, c0=1, aaa="1110", bbb="1010")
    print(s1)#都是str
    '''

    '''
    part3: m bits sum_MUX  √ T-depth = (m)*CSWAP = (m)*4
    
    cin=str(0)
    summ=Q_MUX(nr_qubits=CSA_bits, cin=cin, s0=s0, s1=s1)
    print(summ)
    '''
    '''
    part4:n bits p&g √ T-depth=1*CCNOT
    '''

    '''
    part5:MCC 
    high radix layer, 输入pg,输出 n/radix 个pairs √ T-depth= C_radix_NOT + (radix-1)*CCNOT
    Brent-Kung structure,在high-radix层之后做Brent-Kung,输入high_radix_pg,输出c_radix,c_radix*2,...不需要最高位
    

    High_radix_layer   radix_num 最小radix为2，为1时直接跳过
    p_pairs,g_pairs=High_radix_layer(nr_qubits=add_bit_num,radix=radix_num,p=p,g=g)
    print("p_pairs,g_pairs: ", p_pairs,g_pairs)

    c_pairs=Q_BK(cin=0,p_pairs=p_pairs,g_pairs=g_pairs)#除去 c_最高位，c0为0
    print("c_pairs: ",c_pairs)
    '''





    '''
    part6: whole structure
    
    1. pg                   T-depth= Toffoli_Depth*1
    2. high_radix_layer     T-depth= C_radix_NOT + (radix-1)*CCNOT
    3. B_K(get c,不需要最大位c和最低位c)
    4. put c into MUX(c0提前给了)

    Parallel task：CSA
    '''
    a=''.join(str(random.randint(0, 1)) for _ in range(add_bit_num))
    b= ''.join(str(random.randint(0, 1)) for _ in range(add_bit_num))
        #''.join(str(0) for _ in range(add_bit_num) )
    print("a,b: ",a,b)
    p, g=Q_pg(nr_qubits=add_bit_num,a=a,b=b)
    print("p,g: ",p,g)

    #High_radix_layer   radix_num 最小radix为2，为1时直接跳过
    p_pairs,g_pairs=High_radix_layer(nr_qubits=add_bit_num,radix=radix_num,p=p,g=g)
    print("p_pairs,g_pairs: ", p_pairs,g_pairs)

    c_pairs=Q_BK(cin=0,p_pairs=p_pairs,g_pairs=g_pairs)#除去 c_最高位，c0为0
    #print("c_pairs: ",c_pairs)
    c_pairs='0'+c_pairs#把c0添加进去
    #print("c0+c_pairs: ", c_pairs)
    #CSA
    final_summ=''

    for i in range(math.floor(add_bit_num/radix_num)):
        #0:radix,radix:2*radix,2*radix:3*radix
        aaa=a[(i*radix_num):((i+1)*radix_num)]
        bbb=b[(i*radix_num):((i+1)*radix_num)]
        #print("i",i)
        #print("aaa,bbb: ",aaa,bbb)
        c0_Craig_Gidney,s0= Craig_Gidney.Craig_Gidney_adder(nr_qubits=CSA_bits, c0=0, aaa=aaa, bbb=bbb) #由低位到高位,高位为0
        c1_Craig_Gidney, s1 = Craig_Gidney.Craig_Gidney_adder(nr_qubits=CSA_bits, c0=1, aaa=aaa, bbb=bbb)
        #print("CSA_bits",CSA_bits,"c_pairs[i]",c_pairs[i])
        #print("s0",s0)
        #print("s1", s1)
        summ = Q_MUX(nr_qubits=CSA_bits, cin=c_pairs[i], s0=s0, s1=s1)
        final_summ =final_summ+summ
        #print(summ)
    print("final_summ",final_summ)

    #MUX->summ

if __name__ == "__main__":
    print("add_bit_num=9,radix_num=3")
    Quantum_High_Radix(add_bit_num=9,radix_num=3)
    print("")
    #
    # print("add_bit_num=8, radix_num=4")
    # Quantum_High_Radix(add_bit_num=8, radix_num=4)
    # print("")

    # print("add_bit_num=8, radix_num=2")
    # Quantum_High_Radix(add_bit_num=8, radix_num=2)

    # print("add_bit_num=8, radix_num=2")
    # Quantum_High_Radix(add_bit_num=8, radix_num=2)