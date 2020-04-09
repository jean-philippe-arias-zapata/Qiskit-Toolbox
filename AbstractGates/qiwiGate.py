from qiskit.circuit import Gate


class qiwiGate(Gate):
    """qiwi gate."""
    
    def __init__(self, name, num_qubits, params, least_significant_bit_first=True):
        """Create a new qiwi gate.
        
        Args:
            name (str): the Qobj name of the gate
            num_qubits (int): the number of qubits the gate acts on.
            params (list): a list of parameters.
            least_significant_bit_first (bool): the convention used is the least significant bit first one [Default: True]
            label (str or None): An optional label for the gate [Default: None]
            """
        self.least_significant_bit_first = least_significant_bit_first
        self.definition = None
        super().__init__(name, num_qubits, params, least_significant_bit_first)
            