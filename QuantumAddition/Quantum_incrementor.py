from math import pi
import os
os.chdir('../QFT')
from QFT import quantum_fourier_transform, controlled_quantum_fourier_transform
os.chdir('../QuantumAddition')


# We are in the Qiskit convention, i. e. the least significant bit first convention.
# To go to the most significant bit first convention, you need to :
#   - Add a SWAP gate acting on the target_qubits at the end of the algorithm.


def quantum_incrementor(epsilon, circuit):
    qubits = circuit.qubits
    n_qubits = circuit.n_qubits
    circuit = quantum_fourier_transform(circuit, qubits, inverse=False, bool_swaps=False)
    for i in range(n_qubits):
        circuit.u1(float(pi * epsilon)/2**i , qubits[n_qubits - i - 1])
    circuit = quantum_fourier_transform(circuit, qubits, inverse=True, bool_swaps=False)
    return circuit


def controlled_quantum_incrementor(epsilon, circuit, ctrl_qubits, ancillae_qubits, target_qubits):
    n_target = len(target_qubits)
    circuit = controlled_quantum_fourier_transform(circuit, ctrl_qubits, ancillae_qubits, target_qubits, inverse=False, bool_swaps=False)
    for i in range(n_target):
        circuit.mcu1(float(pi * epsilon)/2**i, ctrl_qubits, target_qubits[n_target - i - 1])
    circuit = controlled_quantum_fourier_transform(circuit, ctrl_qubits, ancillae_qubits, target_qubits, inverse=True, bool_swaps=False)
    return circuit
