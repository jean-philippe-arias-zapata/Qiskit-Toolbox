from qiskit import QuantumRegister
from qiskit.extensions.standard.x import XGate
from AbstractGates.qiwiGate import qiwiGate
from BinaryOracles.Boolean_preparation import to_list
from BitStringTools.Bit_string_tools import XRegionGate

"""

Not working because of uncompatibility between Gate and qiwiGate. Must fix that.


from AbstractGates.ControlGate import ControlGate
class TestOracleGate(qiwiGate):
    Test oracle gate. 
    
    def __init__(self, num_qubits, number, least_significant_bit_first=True):
        self.num_qubits = num_qubits
        self.least_significant_bit_first = least_significant_bit_first
        super().__init__(name=f"Oracle gate(" + str(number) +")", num_qubits=num_qubits, params=[number], least_significant_bit_first=least_significant_bit_first)
        
    def _define(self):
        self.definition = []
        q = QuantumRegister(self.num_qubits)
        self.definition.append((ControlGate(self.num_qubits - 1, self.params[0], XGate(), self.least_significant_bit_first), q, []))
"""


class OracleGate(qiwiGate):
    """Oracle gate.
    
    If the input is:
    - an int, it will be seen as the control register value ;
    - a list, it will be seen as a list of control register values.
    
    """
    
    def __init__(self, num_qubits, list_values, least_significant_bit_first=True):
        self.num_qubits = num_qubits
        self.least_significant_bit_first = least_significant_bit_first
        super().__init__(name=f"Oracle gate(" + str(list_values) +")", num_qubits=num_qubits, params=to_list(list_values), least_significant_bit_first=least_significant_bit_first)

    def _define(self):
        self.definition = []
        q = QuantumRegister(self.num_qubits)
        for number in self.params:
            self.definition.append((XRegionGate(self.num_qubits - 1, number, self.least_significant_bit_first), q[:(self.num_qubits - 1)], []))
            self.definition.append((XGate().control(self.num_qubits - 1), q, []))
            self.definition.append((XRegionGate(self.num_qubits - 1, number, self.least_significant_bit_first), q[:(self.num_qubits - 1)], []))