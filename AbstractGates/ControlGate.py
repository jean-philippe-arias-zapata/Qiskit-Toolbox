from qiskit.circuit import Gate
from qiskit import QuantumRegister
import os
os.chdir("../BitStringTools")
from Bit_string_tools import XRegionGate
os.chdir("../AbstractGates")


#TO BE TESTED


class ControlGate(Gate):
    """Control gate."""
    
    def __init__(self, num_ctrl_qubits, number, gate, least_significant_bit_first=True):
        self.num_qubits = num_ctrl_qubits + gate.num_qubits
        self.number = number
        self.num_ctrl_qubits = num_ctrl_qubits
        self.gate = gate
        super().__init__(name=f"Control-" + gate.name + "(" + str(number) + ")", num_qubits=num_ctrl_qubits + gate.num_qubits, params=[least_significant_bit_first])
        
        
    def _define(self):
        if self.number >= 0 and self.number < 2 ** self.num_ctrl_qubits:
            if len(self.gate.params) != 0:
                if type(self.gate.params[-1]) == bool:
                    if self.params[0] != self.gate.params[-1]:
                        raise NameError("There is an uncompatibility between the desired convention and the " + self.gate.name + " gate convention.")
            self.definition = []
            q = QuantumRegister(self.num_qubits)
            ctrl_q = q[:self.num_ctrl_qubits]
            self.definition.append((XRegionGate(self.num_ctrl_qubits, self.number, self.params[0]), ctrl_q, []))
            self.definition.append((self.gate.control(self.num_ctrl_qubits), q, []))
            self.definition.append((XRegionGate(self.num_ctrl_qubits, self.number, self.params[0]), ctrl_q, [])) 
        else:
            raise NameError("The chosen number is not compatible with the number of control qubits.")