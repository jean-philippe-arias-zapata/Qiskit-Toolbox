from qiskit.circuit import Gate
from qiskit.extensions.standard.u1 import Cu1Gate
from qiskit import QuantumRegister
import os
os.chdir('../QFT')
from QFTGate import QFTGate, DoSwapsGate
os.chdir('../QuantumAddition')
from math import pi     


class QuantumAdderGate(Gate):
    """Quantum Adder gate."""

    def __init__(self, num_qubits, least_significant_bit_first=True):
        self.num_qubits = num_qubits
        super().__init__(name=f"Quantum Adder", num_qubits=num_qubits, params=[least_significant_bit_first])
        
    def _define(self):
        self.definition = []
        if self.num_qubits % 2 == 0:
            q = QuantumRegister(self.num_qubits)
            n = self.num_qubits//2
            x = q[:n]
            y = q[n:]
            if self.params[0]:
                self.definition.append((QFTGate(n, False), y, []))
                for i in range(n):
                    for j in range(n - i):
                        self.definition.append((Cu1Gate(pi / 2 ** j), [x[n - i - 1], y[n - 1 - i - j]], []))
                self.definition.append((QFTGate(n, False).inverse(), y, []))
            else:
                self.definition.append((DoSwapsGate(n), y, []))
                self.definition.append((QFTGate(n, False), y, []))
                for i in range(n):
                    for j in range(n - i):
                        self.definition.append((Cu1Gate(pi / 2 ** j), [x[i], y[n - 1 - i - j]], []))
                self.definition.append((QFTGate(n, False).inverse(), y, []))
                self.definition.append((DoSwapsGate(n), y, []))