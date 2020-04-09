from qiskit import QuantumRegister
from qiwiGate import qiwiGate
import os
os.chdir("../BitStringTools")
from Bit_string_tools import XRegionGate
os.chdir("../AbstractGates")


#TO BE TESTED


class ControlGate(qiwiGate):
    """Control gate."""
    
    def __init__(self, num_ctrl_qubits, number, gate, least_significant_bit_first=True):
        self.num_qubits = num_ctrl_qubits + gate.num_qubits
        self.least_significant_bit_first = least_significant_bit_first
        super().__init__(name=f"Control-" + gate.name + "(" + str(number) + ")", num_qubits=num_ctrl_qubits + gate.num_qubits, params=[num_ctrl_qubits, number, gate])
        
        
    def _define(self):
        if isinstance(self.params[2], qiwiGate) == True:
                if self.least_significant_bit_first != self.params[2].least_significant_bit_first:
                    raise NameError("The desired convention and the " + self.params[2] + "convention are not compatible.")                  
        if self.params[1] >= 0 and self.params[1] < 2 ** self.params[0]:
            self.definition = []
            q = QuantumRegister(self.num_qubits)
            ctrl_q = q[:self.params[0]]
            target_q = q[self.params[0]:]
            self.definition.append((XRegionGate(self.params[0], self.params[1], self.least_significant_bit_first), ctrl_q, []))
            if isinstance(self.params[2], qiwiGate) == False and self.least_significant_bit_first == False:
                q = ctrl_q + target_q[::-1]    
            self.definition.append((self.params[2].control(self.params[0]), q, []))
            if isinstance(self.params[2], qiwiGate) == False and self.least_significant_bit_first == False:
                q = ctrl_q + target_q[::-1]    
            self.definition.append((XRegionGate(self.params[0], self.params[1], self.least_significant_bit_first), ctrl_q, []))
        else:
            raise NameError("The chosen number is not compatible with the number of control qubits.")