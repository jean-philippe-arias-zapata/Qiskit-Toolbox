from qiskit.circuit import Gate
from qiskit.extensions.standard.u1 import Cu1Gate
from qiskit import QuantumRegister
import os
os.chdir('../QFT')
from QFTGate import QFTGate
os.chdir('../QuantumAddition')
from math import pi


# We are in the Qiskit convention, i. e. the least significant bit first convention.
# To go to the most significant bit first convention, you need to :
#   - In line 34, x[n - i - 1] --> x[i];
#   - Add SWAPs gate action on y before the QFTGate and after the QFTGate.inverse.        


class QuantumAdderGate(Gate):
    """Quantum Adder gate."""

    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        super().__init__(name=f"Quantum Adder", num_qubits=num_qubits, params=[])
        
    def _define(self):
        self.definition = []
        if self.num_qubits % 2 == 0:
            q = QuantumRegister(self.num_qubits)
            n = self.num_qubits//2
            x = q[:n]
            y = q[n:]
            self.definition.append((QFTGate(n, False), y, []))
            for i in range(n):
                for j in range(n - i):
                    self.definition.append((Cu1Gate(pi / 2 ** j), [x[n - i - 1], y[n - 1 - i - j]], []))
            self.definition.append((QFTGate(n, False).inverse(), y, []))

        