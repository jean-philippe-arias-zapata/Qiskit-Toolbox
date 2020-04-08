import os
os.chdir('../QFT')
from QFT import quantum_fourier_transform, do_swaps
os.chdir('../QuantumAddition')
from math import pi


def quantum_adder(circuit, to_add_qubits, target_qubits, least_significant_bit_first=True):
    n_qubits = len(target_qubits)
    if n_qubits != len(to_add_qubits):
        raise NameError('The two quantum registers have not the same size.')
    else:
        if least_significant_bit_first:
            circuit = quantum_fourier_transform(circuit, target_qubits, inverse=False, bool_swaps=False)
            for i in range(n_qubits):
                for j in range(n_qubits - i): 
                    circuit.cu1(pi / 2**j, to_add_qubits[n_qubits - i - 1], target_qubits[n_qubits - i - 1 - j])
            circuit = quantum_fourier_transform(circuit, target_qubits, inverse=True, bool_swaps=False)
        else:
            circuit = do_swaps(circuit, target_qubits)
            circuit = quantum_fourier_transform(circuit, target_qubits, inverse=False, bool_swaps=False)
            for i in range(n_qubits):
                for j in range(n_qubits - i): 
                    circuit.cu1(pi / 2**j, to_add_qubits[i], target_qubits[n_qubits - i - 1 - j])
            circuit = quantum_fourier_transform(circuit, target_qubits, inverse=True, bool_swaps=False)
            circuit = do_swaps(circuit, target_qubits)
        return circuit
