from qiskit import QuantumRegister
from qiskit.extensions.standard.h import HGate
from qiskit.extensions.standard.x import XGate
from AbstractGates.qiwiGate import qiwiGate
from BinaryOracles.Boolean_preparation import to_list
from BinaryOracles.OracleGate import OracleGate


class ReflectionGate(qiwiGate):
    """Reflection gate.
    
    If the input is:
    - an int, it will be seen as the control register value ;
    - a list, it will be seen as a list of control register values.
    
    """
    
    def __init__(self, num_qubits, list_values, least_significant_bit_first=True):
        self.num_qubits = num_qubits
        self.least_significant_bit_first = least_significant_bit_first
        super().__init__(name=f"Reflection gate(" + str(list_values) +")", num_qubits=num_qubits, params=to_list(list_values), least_significant_bit_first=least_significant_bit_first)

    def _define(self):
        self.definition = []
        q = QuantumRegister(self.num_qubits)
        self.definition.append((HGate(), [q[self.num_qubits - 1]], []))
        self.definition.append((XGate(), [q[self.num_qubits - 1]], []))
        self.definition.append((HGate(), [q[self.num_qubits - 1]], []))
        self.definition.append((OracleGate(self.num_qubits, self.params, self.least_significant_bit_first), q, []))
        self.definition.append((HGate(), [q[self.num_qubits - 1]], []))
        self.definition.append((XGate(), [q[self.num_qubits - 1]], []))
        self.definition.append((HGate(), [q[self.num_qubits - 1]], []))
        self.definition.append((OracleGate(self.num_qubits, self.params, self.least_significant_bit_first), q, []))