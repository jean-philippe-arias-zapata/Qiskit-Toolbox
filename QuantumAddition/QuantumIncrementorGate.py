from math import pi
import os
os.chdir('../QFT')
from QFTGate import QFTGate, DoSwapsGate
os.chdir('../QuantumAddition')
from qiskit.circuit import Gate
from qiskit import QuantumRegister
from qiskit.extensions.standard.u1 import U1Gate


class QuantumIncrementorGate(Gate):
    """Quantum Incrementor gate."""
    
    def __init__(self, num_qubits, epsilon, least_significant_bit_first=True):
        self.num_qubits = num_qubits
        super().__init__(name=f"Quantum Incrementor({epsilon})", num_qubits=num_qubits, params=[least_significant_bit_first, epsilon])
        
    def _define(self):
        self.definition = []
        q = QuantumRegister(self.num_qubits)
        self.definition.append((QFTGate(self.num_qubits, bool_swaps=False), q, []))
        for i in range(self.num_qubits):
            self.definition.append((U1Gate(float(pi * self.params[1])/2**i), [q[self.num_qubits - i - 1]], []))
        self.definition.append((QFTGate(self.num_qubits, bool_swaps=False).inverse(), q, []))
        if self.params[0] == False:
            self.definition.append((DoSwapsGate(self.num_qubits), q, []))