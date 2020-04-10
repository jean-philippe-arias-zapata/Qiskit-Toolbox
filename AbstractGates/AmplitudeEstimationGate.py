from qiskit import QuantumRegister
from qiwiGate import qiwiGate
from ControlGate import ControlGate
import os 
os.chdir("../QFT")
from QFTGate import QFTGate
os.chdir("../AbstractGates")


#TO BE TESTED


class AmplitudeEstimationGate(qiwiGate):
    """Amplitude Estimation gate."""
    
    def __init__(self, num_accuracy_qubits, grover_gate, least_significant_bit_first=True):
        self.num_qubits = num_accuracy_qubits + grover_gate.num_qubits
        self.least_significant_bit_first = least_significant_bit_first
        super().__init__(name=f"Amplitude Estimation (" + grover_gate.name +")", num_qubits=num_accuracy_qubits + grover_gate.num_qubits, params=[num_accuracy_qubits, grover_gate])
        
    def _define(self):
        self.definition = []
        q = QuantumRegister(self.num_qubits)
        accuracy_qubits = q[:self.params[0]]
        self.definition.append((QFTGate(self.params[0], False, self.least_significant_bit_first), accuracy_qubits, []))
        for i in range(2 ** self.self.params[0]):
            j = 1
            while j <= i:
                self.definition.append((ControlGate(self.params[0], i, self.params[1], not(self.least_significant_bit_first)), q, []))
        self.definition.append((QFTGate(self.params[0], False, self.least_significant_bit_first).inverse(), accuracy_qubits, []))
        
        