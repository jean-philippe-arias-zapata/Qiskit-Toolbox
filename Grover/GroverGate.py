from qiskit import QuantumRegister
from qiskit.extensions.standard.h import HGate
from AbstractGates.qiwiGate import qiwiGate


class GroverGate(qiwiGate):
    """Grover gate."""
    
    def __init__(self, boolean_gate, least_significant_bit_first=True):
        self.num_qubits = boolean_gate.num_qubits
        self.least_significant_bit_first = least_significant_bit_first
        super().__init__(name=f"Grover("+ boolean_gate.name +")", num_qubits=boolean_gate.num_qubits, params=[boolean_gate], least_significant_bit_first=least_significant_bit_first)
        
    def _define(self):
        if isinstance(self.params[0], qiwiGate) == True:
            if self.least_significant_bit_first != self.params[0].least_significant_bit_first:
                raise NameError("The desired convention and the " + self.params[0].name + " convention are not compatible.")
        self.definition = []
        q = QuantumRegister(self.num_qubits)
        for i in range(self.num_qubits):
            self.append((HGate(), [q[i]], []))
        self.append((self.params[0], q, []))
        for i in range(self.num_qubits):
            self.append((HGate(), [q[i]], []))