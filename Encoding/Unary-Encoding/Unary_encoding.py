from qiskit import QuantumCircuit, QuantumRegister
import os
os.chdir('../../Preprocessing')
from data_preparation import is_stochastic_vector
os.chdir('../Encoding/Unary-Encoding')
import numpy as np
from qiskit.aqua.circuits.gates import mcry


def partial_swap(angle, circuit, target_qubits):
    if len(target_qubits) != 2:
        raise NameError('The target qubits list is not of size 2.')
    else:
        ctrl_qubit = target_qubits[0]
        target_qubit = target_qubits[1]
        circuit.cx(target_qubit, ctrl_qubit)
        circuit.cry(angle, ctrl_qubit, target_qubit)
        circuit.cx(target_qubit, ctrl_qubit)
        return circuit


def angles(distribution): #ADD THE POSSIBILITY TO HAVE AN ODD N
    distribution = np.array(distribution)
    n = len(distribution)
    if is_stochastic_vector(distribution) == True and n % 2 == 0:        
        angles = []        
        for i in range(n - 1):
            i = i + 1
            if i < n / 2:
                angles.append(2 * np.arctan2(np.sqrt(np.sum(distribution[0:i])), np.sqrt(distribution[i])))   
            elif i == n / 2 :
                inter = int(n / 2)
                angles.append(2 * np.arctan2(np.sqrt(1 - np.sum(distribution[inter:n])), np.sqrt(np.sum(distribution[inter:n]))))
            else : 
                angles.append(2 * np.arctan2(np.sqrt(np.sum(distribution[i:n])), np.sqrt(distribution[i - 1])))
        return angles
    else :
        raise NameError("The input vector is not a probability distribution or its dimension is not a multiple of 2.")
        

def unary_encoding(distribution, circuit = None, distribution_qubits = None):
    n_qubits = len(distribution)
    if distribution_qubits == None:
        if circuit == None: 
            distribution_qubits = QuantumRegister(n_qubits)
            circuit = QuantumCircuit(distribution_qubits)
        else:
            distribution_qubits = circuit.qubits
    else:
        if len(distribution_qubits) != n_qubits:
            raise NameError('The number of distribution qubits is incompatible with the distribution size.')
    theta = angles(distribution)
    inter = int(n_qubits / 2)
    circuit.x(distribution_qubits[inter])
    circuit = partial_swap(theta[inter - 1], circuit, distribution_qubits[inter - 1], distribution_qubits[inter])
    for step in range(inter - 1):
        step = step + 1
        circuit = partial_swap(theta[inter - 1 - step], circuit, distribution_qubits[inter - 1 - step], distribution_qubits[inter - step])
        circuit = partial_swap(theta[inter - 1 + step], circuit, distribution_qubits[inter - 1 + step], distribution_qubits[inter + step])
    return circuit, distribution_qubits


### CONTROLLED VERSIONS
    

def controlled_partial_swap(angle, circuit, ancillae_qubits, control_qubits, target_qubits):
    if len(target_qubits) != 2:
        raise NameError('The target qubits list is not of size 2.')
    else:
        ctrl_qubit = target_qubits[0]
        target_qubit = target_qubits[1]  
        circuit.mcmt(list(control_qubits) + [target_qubit], ancillae_qubits[1:], QuantumCircuit.cx, [ctrl_qubit])
        circuit.mcry(angle, list(control_qubits) + [ctrl_qubit], target_qubit, None, 'noancilla')
        circuit.mcmt(list(control_qubits) + [target_qubit], ancillae_qubits[1:], QuantumCircuit.cx, [ctrl_qubit])
        return circuit
    
    
def controlled_unary_encoding(distribution, circuit, ancillae_qubits, control_qubits, distribution_qubits = None): #on veut aussi retourner distribution_qubits, modifier ce qui en découle
    theta = angles(distribution)
    n_qubits = len(distribution)
    if distribution_qubits != None:
        if len(distribution_qubits) != n_qubits:
            raise NameError('The number of the distribution qubits is incompatible with the distribution size.')
    else:
        distribution_qubits = QuantumRegister(n_qubits)
        circuit.add_register(distribution_qubits)
    inter = int(n_qubits / 2)
    circuit.mcmt(control_qubits, ancillae_qubits[1:], QuantumCircuit.cx, [distribution_qubits[inter]])
    circuit = controlled_partial_swap(theta[inter - 1], circuit, ancillae_qubits, control_qubits, [distribution_qubits[inter - 1], distribution_qubits[inter]])
    for step in range(inter - 1):
        step = step + 1
        circuit = controlled_partial_swap(theta[inter - 1 - step], circuit, ancillae_qubits, control_qubits, [distribution_qubits[inter - step - 1], distribution_qubits[inter - step]])
        circuit = controlled_partial_swap(theta[inter - 1 + step], circuit, ancillae_qubits, control_qubits, [distribution_qubits[inter + step - 1], distribution_qubits[inter + step]])
    return circuit, distribution_qubits


def inverse_controlled_unary_encoding(distribution, circuit, ancillae_qubits, control_qubits, distribution_qubits):
    theta = angles(distribution)
    n_qubits = len(distribution)
    if len(distribution_qubits) != n_qubits:
        raise NameError('The number of threshold qubits is incompatible with the distribution size.')
    else:
        inter = int(n_qubits / 2)
        for step in range(inter - 1):
            circuit = controlled_partial_swap(-theta[step], circuit, ancillae_qubits, control_qubits, [distribution_qubits[step], distribution_qubits[step + 1]])
            circuit = controlled_partial_swap(-theta[n_qubits - step - 2], circuit, ancillae_qubits, control_qubits, [distribution_qubits[n_qubits - step - 2], distribution_qubits[n_qubits - step - 1]])
        circuit = controlled_partial_swap(-theta[inter - 1], circuit, ancillae_qubits, control_qubits, [distribution_qubits[inter - 1], distribution_qubits[inter]])
        circuit.mcmt(control_qubits, ancillae_qubits[1:], QuantumCircuit.cx, [distribution_qubits[inter]])
        return circuit