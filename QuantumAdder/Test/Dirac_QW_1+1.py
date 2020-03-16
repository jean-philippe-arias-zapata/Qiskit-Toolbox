from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, execute, Aer
from Quantum_adder import controlled_quantum_adder


def Dirac_QW_spatial_translation(epsilon, circuit, spin_qubit, position_qubits, ancilla_qubit):
    circuit = controlled_quantum_adder(- epsilon, circuit, spin_qubit, ancilla_qubit, position_qubits)
    circuit.x(spin_qubit)
    circuit = controlled_quantum_adder(epsilon, circuit, spin_qubit, ancilla_qubit, position_qubits)
    circuit.x(spin_qubit)
    return circuit


def Dirac_QW_mass_mixing(epsilon, mass, circuit, spin_qubit):
    circuit.rx(2 * mass * epsilon, spin_qubit)
    return circuit


def Dirac_QW_step(epsilon, mass, circuit, spin_qubit, position_qubits, ancilla_qubit):
    circuit = Dirac_QW_mass_mixing(epsilon, mass, circuit, spin_qubit)
    circuit = Dirac_QW_spatial_translation(epsilon, circuit, spin_qubit, position_qubits, ancilla_qubit)
    return circuit
    

n_qubits_position = 3
epsilon = 1
mass = 0.1


spin_qubit = QuantumRegister(1)
ancilla_qubit = QuantumRegister(1)
position_qubits = QuantumRegister(n_qubits_position)
clbits = ClassicalRegister(2 + n_qubits_position)

circuit = QuantumCircuit(position_qubits, clbits)
circuit.add_register(spin_qubit)
circuit.add_register(ancilla_qubit)


circuit = Dirac_QW_step(epsilon, mass, circuit, spin_qubit, position_qubits, ancilla_qubit)
circuit.measure(circuit.qubits, clbits)

backend = Aer.get_backend('qasm_simulator')

job_sim = execute(circuit, backend, shots=10000)

sim_result = job_sim.result()
print(sim_result.get_counts(circuit))