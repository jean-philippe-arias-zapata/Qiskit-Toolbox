import os
os.chdir('../QFT')
from QFT import quantum_fourier_transform
os.chdir('../QuantumAddition')
from math import pi


# We are in the Qiskit convention, i. e. the least significant bit first convention.
# To go to the most significant bit first convention, you need to :
#   - In line 23, to_add_qubits[n_qubits - i - 1] --> to_add_qubits[i];
#   - Add SWAPs gate action on y before the QFT and after the inverse of QFT. 


def quantum_adder(circuit, to_add_qubits, target_qubits):
    n_qubits = len(target_qubits)
    if n_qubits != len(to_add_qubits):
        raise NameError('The two quantum registers have not the same size.')
    else:
        circuit = quantum_fourier_transform(circuit, target_qubits, inverse=False, bool_swaps=False)
        for i in range(n_qubits):
            for j in range(n_qubits - i): 
                circuit.cu1(pi / 2**j, to_add_qubits[n_qubits - i - 1], target_qubits[n_qubits - i - 1 - j])
        circuit = quantum_fourier_transform(circuit, target_qubits, inverse=True, bool_swaps=False)
        return circuit