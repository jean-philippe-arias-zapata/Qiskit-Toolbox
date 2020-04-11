from qiskit import QuantumRegister
from qiskit.extensions.standard.u1 import U1Gate
from AbstractGates.qiwiGate import qiwiGate
from QFT.QFTGate import QFTGate
from math import pi



class QuantumIncrementorGate(qiwiGate):
    """Quantum Incrementor gate."""
    
    def __init__(self, num_qubits, epsilon, least_significant_bit_first=True):
        self.num_qubits = num_qubits
        self.least_significant_bit_first = least_significant_bit_first
        super().__init__(name=f"Quantum Incrementor({epsilon})", num_qubits=num_qubits, params=[epsilon], least_significant_bit_first=least_significant_bit_first)
        
    def _define(self):
        self.definition = []
        q = QuantumRegister(self.num_qubits)
        if self.least_significant_bit_first == False:
            q = q[::-1]
        self.definition.append((QFTGate(self.num_qubits, bool_swaps=False), q, []))
        for i in range(self.num_qubits):
            self.definition.append((U1Gate(float(pi * self.params[0])/2**i), [q[self.num_qubits - i - 1]], []))
        self.definition.append((QFTGate(self.num_qubits, bool_swaps=False).inverse(), q, []))
        if self.least_significant_bit_first == False:
            q = q[::-1]