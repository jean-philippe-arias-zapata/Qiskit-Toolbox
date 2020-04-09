from qiskit.circuit import Gate
from qiskit import QuantumRegister
from ControlGate import ControlGate
import os 
os.chdir("../QFT")
from QFTGate import QFTGate
os.chdir("../AbstractGates")


#TO BE TESTED


class AmplitudeEstimationGate(Gate):
    """Amplitude Estimation gate."""
    
    def __init__(self, num_accuracy_qubits, grover_gate):
        self.num_qubits = num_accuracy_qubits + grover_gate.num_qubits
        self.num_accuracy_qubits = num_accuracy_qubits
        self.grover_gate = grover_gate
        if len(grover_gate.params) == 0:
            super().__init__(name=f"Amplitude Estimation", num_qubits=num_accuracy_qubits + grover_gate.num_qubits, params=[True])
        else:
            if grover_gate.params[-1] == False:
                super().__init__(name=f"Amplitude Estimation", num_qubits=num_accuracy_qubits + grover_gate.num_qubits, params=[False])
            else:
                super().__init__(name=f"Amplitude Estimation", num_qubits=num_accuracy_qubits + grover_gate.num_qubits, params=[True])
        
    def _define(self):
        self.definition = []
        q = QuantumRegister(self.num_qubits)
        accuracy_qubits = q[:self.num_accuracy_qubits]
        self.definition.append((QFTGate(self.num_accuracy_qubits), accuracy_qubits, []))
        for i in range(2 ** self.num_accuracy_qubits):
            j = 1
            while j <= i:
                self.definition.append((ControlGate(self.num_accuracy_qubits, i, self.grover_gate), q, []))
        self.definition.append((QFTGate(self.num_accuracy_qubits).inverse(), accuracy_qubits, []))
        
        