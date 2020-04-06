from qiskit.circuit import Gate
from qiskit.extensions.standard.u1 import Cu1Gate
from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister, execute, Aer
import os
os.chdir('../QFT')
from QFTGate import QFTGate
os.chdir('../QuantumAddition')
from math import pi


class QuantumAdderGate(Gate):
    """Quantum Adder gate."""

    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        super().__init__(name=f"Quantum Adder", num_qubits=num_qubits, params=[])
        
    def _define(self):
        self.definition = []
        if self.num_qubits % 2 == 0:
            q = QuantumRegister(self.num_qubits)
            n = self.num_qubits//2
            x = q[:n]
            y = q[n:]
            self.definition.append((QFTGate(n), y, []))
            for i in range(n):
                for j in range(n - i):
                    self.definition.append((Cu1Gate(pi / 2 ** j), [x[i], y[n - 1 - i - j]], []))
            self.definition.append((QFTGate(n).inverse(), y, []))

            
qr = QuantumRegister(4)
cl = ClassicalRegister(2)
circ = QuantumCircuit(qr, cl)
circ.x(qr[0])
circ.append(QuantumAdderGate(4), qr, [])
circ.measure(qr[2:], cl)

backend = Aer.get_backend('qasm_simulator')

job_sim = execute(circ, backend, shots=10000)

sim_result = job_sim.result()
print(sim_result.get_counts(circ))

        