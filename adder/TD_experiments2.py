import cirq
import mathematics
import utils.counting_utils as cu
from qramcircuits.toffoli_decomposition import *
import adder.gidney as gidney
import adder.cuccaro as cuccaro
import adder.inDraper as inDraper
import adder.outDraper as outDraper
import adder.takahashi as takahashi

def add(a, b, n, Adder,t=-1):
    A = [cirq.NamedQubit("A" + str(i)) for i in range(n)]
    B = [cirq.NamedQubit("B" + str(i)) for i in range(n)]

    circuit = cirq.Circuit()
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
    circuit.append(cirq.measure(maxancilla, key="result"))

    return circuit

def maxsub2(a, b, n, Adder,t=-1):

    A = [cirq.NamedQubit("A" + str(i)) for i in range(n)]
    B = [cirq.NamedQubit("B" + str(i)) for i in range(n)]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(A[i]) for i in range(n))
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
    circuit.append(cirq.measure(maxancilla, key="result"))

    return circuit

n=1
a=0b1
b=0b1

s = cirq.Simulator()
circuit=add(a,b,n, gidney.Adder)
#circuit=maxsub1(a,b,n, gidney.Adder)
#circuit=add(a,b,n, takahashi.Adder)
TD_circuit = cirq.Circuit(
        ToffoliDecomposition.construct_decomposed_moments(circuit.moments, ToffoliDecompType.ONE_ANCILLA_TDEPTH_2))
results = s.simulate(circuit)
#print(circuit)
#print(TD_circuit)
output = results.measurements['result']
print(output[::-1])
print(f"T_count : {int(cu.count_t_of_circuit(TD_circuit))}")
print(f"T_depth : {int(cu.count_t_depth_of_circuit(TD_circuit))}")
'''
print(f"Toffoli_depth : {int(cu.count_toffoli_depth_of_circuit(TD_circuit))}")
print(f"Toffoli_count : {int(cu.count_toffoli_of_circuit(TD_circuit))}")
print(f"CNOT_count : {int(cu.count_cnot_of_circuit(circuit))}")
print(f"H_count : {int(cu.count_h_of_circuit(circuit))}")
'''
print(f"Qubit_count : {int(cirq.num_qubits(TD_circuit))}")

