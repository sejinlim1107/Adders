import cirq
import utils.counting_utils as cu
import adder.gidney as gidney
import adder.cuccaro as cuccaro
import adder.cuccaro_2CNOT as cuccaro_2CNOT
import adder.inDraper as inDraper
import adder.outDraper as outDraper
import adder.takahashi as takahashi


def add(a, b, n, Adder,t=-1):
    A = [cirq.NamedQubit("A" + str(i)) for i in range(n)]
    B = [cirq.NamedQubit("B" + str(i)) for i in range(n)]

    circuit = cirq.Circuit()
    if rctr != 1:
        for i in range(n):
            if ((a >> i) & 1 == 1):
                circuit.append(cirq.X(A[i]))
            if ((b >> i) & 1 == 1):
                circuit.append(cirq.X(B[i]))

    if (t == -1):
        adder = Adder(A, B)
    else:
        adder = Adder(A, B, t)
    circuit.append(adder.circuit)
    #circuit.append(cirq.measure(A, key='A'))
    #circuit.append(cirq.measure(B, key='B'))
    if rctr != 1:
        circuit.append(cirq.measure(adder.result, key="result"))

    return circuit

def sub1(a, b, n, Adder, t=-1):

    A = [cirq.NamedQubit("A" + str(i)) for i in range(n)]
    B = [cirq.NamedQubit("B" + str(i)) for i in range(n)]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(A[i]) for i in range(n))
    for i in range(n):
        if ((a >> i) & 1 == 1):
            circuit.append(cirq.X(A[i]))
        if ((b >> i) & 1 == 1):
            circuit.append(cirq.X(B[i]))
    if (t == -1):
        adder = Adder(A, B)
    else:
        adder = Adder(A, B, t)
    circuit.append(adder.circuit)

    circuit.append(cirq.X(adder.result[i]) for i in range(n))
    circuit.append(cirq.measure(adder.result, key="result"))

    return circuit

def maxsub1(a, b, n, Adder,t=-1):
    A = [cirq.NamedQubit("A" + str(i)) for i in range(n)]
    B = [cirq.NamedQubit("B" + str(i)) for i in range(n)]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(A[i]) for i in range(n))

    if rctr != 1:
        for i in range(n):
            if ((a >> i) & 1 == 1):
                circuit.append(cirq.X(A[i]))
            if ((b >> i) & 1 == 1):
                circuit.append(cirq.X(B[i]))

    if(t ==-1):
        adder = Adder(A, B)
    else:
        adder = Adder(A, B, t)
    circuit.append(adder.circuit)

    circuit.append(cirq.X(adder.result[i]) for i in range(n+1))
    maxancilla = [cirq.NamedQubit("max" + str(i)) for i in range(n+1)]
    circuit.append(cirq.TOFFOLI(adder.result[-1], adder.result[i], maxancilla[i]) for i in range(0,n))
    if rctr != 1:
        circuit.append(cirq.measure(maxancilla, key="result"))

    return circuit

def maxsub2(a, b, n, Adder,t=-1): # T-depth 줄이기

    A = [cirq.NamedQubit("A" + str(i)) for i in range(n)]
    B = [cirq.NamedQubit("B" + str(i)) for i in range(n)]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(A[i]) for i in range(n))
    if rctr != 1:
        for i in range(n):
            if ((a >> i) & 1 == 1):
                circuit.append(cirq.X(A[i]))
            if ((b >> i) & 1 == 1):
                circuit.append(cirq.X(B[i]))
    if(t ==-1):
        adder = Adder(A, B)
    else:
        adder = Adder(A, B, t)
    circuit.append(adder.circuit)

    circuit.append(cirq.X(adder.result[i]) for i in range(n+1))
    maxancilla = [cirq.NamedQubit("max" + str(i)) for i in range(n+1)]
    ancillas = [cirq.NamedQubit("ancillas" + str(i)) for i in range(n-1)]
    circuit.append(cirq.CNOT(adder.result[-1], ancillas[i]) for i in range(n-1))
    circuit.append(cirq.TOFFOLI(ancillas[i], adder.result[i], maxancilla[i]) for i in range(0,n-1))
    circuit.append(cirq.TOFFOLI(adder.result[-1], adder.result[n-1], maxancilla[n-1]))
    if rctr != 1:
        circuit.append(cirq.measure(maxancilla, key="result"))

    return circuit

'''
n=7
a=15
b=1
'''

n=4
a=0b1100
b=0b1111

rctr = 0

s = cirq.Simulator()
circuit=add(a,b,n, takahashi.Adder)
results = s.simulate(circuit)
output = results.measurements['result']
print(output[::-1])
print(f"T_depth : {int(cu.count_t_depth_of_circuit(circuit))}")
print(f"T_count : {int(cu.count_t_of_circuit(circuit))}")
print(f"Toffoli_depth : {int(cu.count_toffoli_depth_of_circuit(circuit))}")
print(f"Toffoli_count : {int(cu.count_toffoli_of_circuit(circuit))}")
print(f"CNOT_count : {int(cu.count_cnot_of_circuit(circuit))}")
print(f"H_count : {int(cu.count_h_of_circuit(circuit))}")
print(f"Qubit_count : {int(cirq.num_qubits(circuit))}")