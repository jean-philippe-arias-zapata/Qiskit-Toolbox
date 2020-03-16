from qiskit import QuantumCircuit
from math import pi
#from qiskit.aqua.circuits.fourier_transform_circuits import FourierTransformCircuits: library to use


def do_swaps(circuit, qubits):
    n_qubits = len(qubits)
    for i in range(n_qubits // 2):
        circuit.cx(qubits[i], qubits[n_qubits - i - 1])
        circuit.cx(qubits[n_qubits - i - 1], qubits[i])
        circuit.cx(qubits[i], qubits[n_qubits - i - 1])
    return circuit


def quantum_fourier_transform(circuit, qubits, inverse=False, bool_swaps=True):
    n_qubits = len(qubits)
    if inverse == False:
        for i in range(n_qubits):
            circuit.h(qubits[i])
            for distance in range(n_qubits - i - 1):
                distance = distance + 1
                circuit.cu1(pi / 2**distance, qubits[distance + i], qubits[i])
    else:
        for i in range(n_qubits):
            i = n_qubits - 1 - i
            for distance in range(n_qubits - i - 1):
                distance = distance + 1
                circuit.cu1(- pi / 2**distance, qubits[distance + i], qubits[i])
            circuit.h(qubits[i])
    if bool_swaps:
        circuit = do_swaps(circuit, qubits)
    return circuit


def controlled_quantum_fourier_transform(circuit, ctrl_qubits, ancillae_qubits, target_qubits, inverse=False, bool_swaps=True): 
    if ctrl_qubits == None:
        circuit = quantum_fourier_transform(circuit, circuit.qubits, inverse)
    else:
          n_target = len(target_qubits)
          if inverse == False:
              for i in range(n_target):
                  circuit.mcmt(ctrl_qubits, ancillae_qubits, QuantumCircuit.ch, [target_qubits[i]])
                  for distance in range(n_target - i - 1):
                      distance = distance + 1
                      inter_ctrl = [target_qubits[distance + i]]
                      for ctrl in ctrl_qubits:
                          inter_ctrl.append(ctrl)
                      circuit.mcu1(pi / 2**distance, inter_ctrl, target_qubits[i])
          else:
              for i in range(n_target):
                  i = n_target - 1 - i
                  for distance in range(n_target - i - 1):
                      distance = distance + 1
                      inter_ctrl = [target_qubits[distance + i]]
                      for ctrl in ctrl_qubits:
                          inter_ctrl.append(ctrl)
                      circuit.mcu1(- pi / 2**distance, inter_ctrl, target_qubits[i])
                  circuit.mcmt(ctrl_qubits, ancillae_qubits, QuantumCircuit.ch, [target_qubits[i]])
    if bool_swaps:
        circuit = do_swaps(circuit, target_qubits)
    return circuit