from math import pi
import os
os.chdir('../QFT')
from QFTGate import QFTGate
os.chdir('../QuantumAddition')
from qiskit.circuit import Gate
from qiskit import QuantumRegister
from qiskit.extensions.standard.u1 import U1Gate


# We are in the Qiskit convention, i. e. the least significant bit first convention.
# To go to the most significant bit first convention, you need to :
#   - Add a SWAP gate acting on q at the end of the algorithm.  


class QuantumIncrementorGate(Gate):
    """Quantum Incrementor gate."""
    
    def __init__(self, num_qubits, epsilon):
        self.num_qubits = num_qubits
        super().__init__(name=f"Quantum Incrementor({epsilon})", num_qubits=num_qubits, params=[epsilon])
        
    def _define(self):
        self.definition = []
        q = QuantumRegister(self.num_qubits)
        self.definition.append((QFTGate(self.num_qubits, bool_swaps=False), q, []))
        for i in range(self.num_qubits):
            self.definition.append((U1Gate(float(pi * self.params[0])/2**i), [q[self.num_qubits - i - 1]], []))
        self.definition.append((QFTGate(self.num_qubits, bool_swaps=False).inverse(), q, []))
