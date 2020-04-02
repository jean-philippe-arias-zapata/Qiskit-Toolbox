from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Gate
from qiskit.extensions.standard.x import XGate


def to_bin(region, step):
    to_bin = format(region, 'b')
    if len(to_bin) != step:
        difference = step - len(to_bin)
        while(difference != 0):
            to_bin = '0' + to_bin
            difference = difference - 1
    return to_bin


def to_number(string): #Attention aux conventions de Python et Qiskit
    number = 0 
    n = len(string)
    for i in range(n):
        number = number + int(string[n - i - 1]) * 2 ** i
    return number


def x_gates_region(circuit, qubits, string):
    n_qubits = len(qubits)
    for i in range(len(string)):
        if string[i] == '0':
              circuit.x(qubits[n_qubits - i - 1])
    return circuit 


class XRegionGate(Gate):
    """X-Region gate. """
    
    def __init__(self, num_qubits, string):
        self.num_qubits = num_qubits
        self.string = string
        super().__init__(name=f"XRegion({string})", num_qubits=num_qubits, params=[string])
    
    def _define(self):
        self.definition = []
        q = QuantumRegister(self.num_qubits)
        for i in range(len(self.string)):
            if self.string[i] == '0':
                self.definition.append((XGate(), [q[self.num_qubits - i - 1]], []))