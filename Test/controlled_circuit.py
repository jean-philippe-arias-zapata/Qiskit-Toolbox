from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit.circuit.gate import control
from circuit_to_gate import circuit_to_gate

def controlled_circuit(circuit, num_ctrl_qubits, label=None):
    gate = circuit_to_gate(circuit)
    gate = control(num_ctrl_qubits, label=None).gate
    return circuit