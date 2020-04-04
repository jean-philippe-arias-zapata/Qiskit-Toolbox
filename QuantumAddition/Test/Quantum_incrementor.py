from math import pi
import os
os.chdir('../../QFT')
from QFT import quantum_fourier_transform, controlled_quantum_fourier_transform
os.chdir('../QuantumAdder/Test')


def quantum_incrementor(epsilon, circuit):
    qubits = circuit.qubits
    n_qubits = circuit.n_qubits
    circuit = quantum_fourier_transform(circuit, qubits)
    for i in range(n_qubits):
        circuit.u1(float(pi * epsilon)/2**i , qubits[n_qubits - i - 1])
    circuit = quantum_fourier_transform(circuit, qubits, inverse=True)
    return circuit


def controlled_quantum_incrementor(epsilon, circuit, ctrl_qubits, ancillae_qubits, target_qubits):
    n_target = len(target_qubits)
    circuit = controlled_quantum_fourier_transform(circuit, ctrl_qubits, ancillae_qubits, target_qubits)
    for i in range(n_target):
        circuit.mcu1(float(pi * epsilon)/2**i, ctrl_qubits, target_qubits[n_target - i - 1])
    circuit = controlled_quantum_fourier_transform(circuit, ctrl_qubits, ancillae_qubits, target_qubits, inverse=True)
    return circuit
