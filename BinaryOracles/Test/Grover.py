from qiskit import QuantumRegister, QuantumCircuit


### UNARY LOWER THAN


def exact_lower_than_binary_oracle(circuit, ancillae_qubits, threshold_qubits, threshold):
    threshold = int(threshold)
    main_ancilla_qubit = ancillae_qubits[0]
    n_qubits = len(threshold_qubits)     
    if len(ancillae_qubits) == 1:
        if threshold > n_qubits - 1:
            circuit.x(main_ancilla_qubit)
        elif threshold <= 0:
                raise NameError('This threshold cannot be studied because of lack of ancillae qubits.')
        else:
            circuit.x(threshold_qubits[threshold:n_qubits])
            circuit.mcmt(threshold_qubits[threshold:n_qubits], threshold_qubits[0:threshold], QuantumCircuit.cx, main_ancilla_qubit)
            circuit.x(threshold_qubits[threshold:n_qubits])
    else:
        if threshold > n_qubits - 1:
            circuit.x(main_ancilla_qubit)
        else:
            circuit.x(threshold_qubits[max(0, threshold):n_qubits])
            circuit.mcmt(threshold_qubits[max(0, threshold):n_qubits], ancillae_qubits[1:], QuantumCircuit.cx, main_ancilla_qubit)
            circuit.x(threshold_qubits[max(0, threshold):n_qubits])
    return circuit


def reflection_exact_lower_than(circuit, ancillae_qubits, threshold_qubits, threshold):
    main_ancilla_qubit = ancillae_qubits[0]
    circuit.x(main_ancilla_qubit)
    circuit.h(main_ancilla_qubit)
    circuit = exact_lower_than_binary_oracle(circuit, ancillae_qubits, threshold_qubits, threshold)
    circuit.h(main_ancilla_qubit)
    circuit.x(main_ancilla_qubit)
    return circuit


### CONTROLLED VERSIONS
    

def controlled_exact_lower_than_binary_oracle(circuit, ancillae_qubits, control_qubits, threshold_qubits, threshold): ### FAIRE ATTENTION A LA SOMME D'UN ELEMENT AVEC UNE LISTE LIGNE 53
    threshold = int(threshold)
    second_ancilla_qubit = ancillae_qubits[1]
    n_qubits = len(threshold_qubits)     
    if len(ancillae_qubits) == 1:
        raise NameError('This threshold cannot be studied because of lack of ancillae qubits.')
    else:
        if threshold > n_qubits - 1:
            circuit.mcmt(control_qubits, ancillae_qubits[2:], QuantumCircuit.cx, second_ancilla_qubit)
        else:
            if len(control_qubits) != 1:
                circuit.mcmt(control_qubits, ancillae_qubits[2:], QuantumCircuit.cx, threshold_qubits[max(0, threshold):n_qubits])
                circuit.mcmt(control_qubits + threshold_qubits[max(0, threshold):n_qubits], ancillae_qubits[2:], QuantumCircuit.cx, second_ancilla_qubit)
                circuit.mcmt(control_qubits, ancillae_qubits[2:], QuantumCircuit.cx, threshold_qubits[max(0, threshold):n_qubits])
            else:
                circuit.mcmt(control_qubits, ancillae_qubits[2:], QuantumCircuit.cx, threshold_qubits[max(0, threshold):n_qubits])
                circuit.mcmt([control_qubits] + threshold_qubits[max(0, threshold):n_qubits], ancillae_qubits[2:], QuantumCircuit.cx, second_ancilla_qubit)
                circuit.mcmt(control_qubits, ancillae_qubits[2:], QuantumCircuit.cx, threshold_qubits[max(0, threshold):n_qubits])
    return circuit


def controlled_reflection_exact_lower_than(circuit, ancillae_qubits, threshold_qubits, control_qubits, threshold):
    second_ancilla_qubit = ancillae_qubits[1]
    circuit.mcmt(control_qubits, ancillae_qubits[2:], QuantumCircuit.cx, second_ancilla_qubit)
    circuit.mcmt(control_qubits, ancillae_qubits[2:], QuantumCircuit.ch, second_ancilla_qubit)
    circuit = controlled_exact_lower_than_binary_oracle(circuit, ancillae_qubits, threshold_qubits, control_qubits, threshold)
    circuit.mcmt(control_qubits, ancillae_qubits[2:], QuantumCircuit.ch, second_ancilla_qubit)
    circuit.mcmt(control_qubits, ancillae_qubits[2:], QuantumCircuit.cx, second_ancilla_qubit)
    return circuit