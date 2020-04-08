from math import pi
import os
os.chdir('../QFT')
from QFT import quantum_fourier_transform, controlled_quantum_fourier_transform, do_swaps, controlled_do_swaps
os.chdir('../QuantumAddition')


def quantum_incrementor(epsilon, circuit, least_significant_bit_first=True):
    qubits = circuit.qubits
    n_qubits = circuit.n_qubits
    circuit = quantum_fourier_transform(circuit, qubits, inverse=False, bool_swaps=False)
    for i in range(n_qubits):
        circuit.u1(float(pi * epsilon)/2**i , qubits[n_qubits - i - 1])
    circuit = quantum_fourier_transform(circuit, qubits, inverse=True, bool_swaps=False)
    if least_significant_bit_first == False:
        circuit = do_swaps(circuit, qubits)
    return circuit


def controlled_quantum_incrementor(epsilon, circuit, ctrl_qubits, ancillae_qubits, target_qubits, least_significant_bit_first=True):
    n_target = len(target_qubits)
    circuit = controlled_quantum_fourier_transform(circuit, ctrl_qubits, ancillae_qubits, target_qubits, inverse=False, bool_swaps=False)
    for i in range(n_target):
        circuit.mcu1(float(pi * epsilon)/2**i, ctrl_qubits, target_qubits[n_target - i - 1])
    circuit = controlled_quantum_fourier_transform(circuit, ctrl_qubits, ancillae_qubits, target_qubits, inverse=True, bool_swaps=False)
    if least_significant_bit_first == False:
        circuit = controlled_do_swaps(circuit, target_qubits)
    return circuit