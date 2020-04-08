from qiskit.circuit import Gate
from qiskit import QuantumRegister
import os
os.chdir("../BitStringTools")
from Bit_string_tools import XRegionGate
os.chdir("../AbstractGates")


class ControlGate(Gate):
    
    def __init__(self, num_ctrl_qubits, number, gate):
        self.num_qubits = num_ctrl_qubits + gate.num_qubits
        self.number = number
        self.num_ctrl_qubits = num_ctrl_qubits
        self.gate = gate
        if len(gate.params) == 0:
            super().__init__(name=f"Control-" + gate.name + "(" + str(number) + ")", num_qubits=num_ctrl_qubits + gate.num_qubits, params=[True])
        else:
            if gate.params[-1] == False:
                super().__init__(name=f"Control-" + gate.name + "(" + str(number) + ")", num_qubits=num_ctrl_qubits + gate.num_qubits, params=[False])
            else:
                super().__init__(name=f"Control-" + gate.name + "(" + str(number) + ")", num_qubits=num_ctrl_qubits + gate.num_qubits, params=[True])
        
    def _define(self):
        if self.number >= 0 and self.number < 2 ** self.num_ctrl_qubits:
            self.definition = []
            q = QuantumRegister(self.num_qubits)
            ctrl_q = q[:self.num_ctrl_qubits]
            self.definition.append((XRegionGate(self.num_ctrl_qubits, self.number, self.params[0]), ctrl_q, []))
            self.definition.append((self.gate.control(self.num_ctrl_qubits), q, []))
            self.definition.append((XRegionGate(self.num_ctrl_qubits, self.number, self.params[0]), ctrl_q, []))
            
        else:
            raise NameError("The chosen number is not compatible with the number of control qubits.")