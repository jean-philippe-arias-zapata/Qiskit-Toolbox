from qiskit.extensions.standard.u1 import Cu1Gate
from qiskit import QuantumRegister
import os
os.chdir('../AbstractGates')
from qiwiGate import qiwiGate
os.chdir('../QFT')
from QFTGate import QFTGate
os.chdir('../QuantumAddition')
from math import pi     


class QuantumAdderGate(qiwiGate):
    """Quantum Adder gate."""

    def __init__(self, num_qubits, least_significant_bit_first=True):
        self.num_qubits = num_qubits
        self.least_significant_bit_first = least_significant_bit_first
        super().__init__(name=f"Quantum Adder", num_qubits=num_qubits, params=[], least_significant_bit_first=least_significant_bit_first)
        
    def _define(self):
        self.definition = []
        if self.num_qubits % 2 == 0:
            q = QuantumRegister(self.num_qubits)
            n = self.num_qubits//2
            x = q[:n]
            y = q[n:]
            if self.least_significant_bit_first == False:
                x = x[::-1]
                y = y[::-1]
            self.definition.append((QFTGate(n, False), y, []))
            for i in range(n):
                for j in range(n - i):
                    self.definition.append((Cu1Gate(pi / 2 ** j), [x[n - i - 1], y[n - 1 - i - j]], []))
            self.definition.append((QFTGate(n, False).inverse(), y, []))
            if self.least_significant_bit_first == False:
                x = x[::-1]
                y = y[::-1]