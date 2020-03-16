from sympy import Matrix, symbols, eye, cos, sin
from sympy.physics.quantum import TensorProduct


n_qubits = 10


X = Matrix([[0, 1], [1, 0]])
do_not = Matrix([[1, 0], [0, 0]])
do = Matrix([[0, 0], [0, 1]])
ctrl_x = TensorProduct(do_not, eye(2)) + TensorProduct(do, X)


def rot(angle):
    return Matrix([[cos(angle /2), -sin(angle / 2)], [sin(angle / 2), cos(angle / 2)]])


def ctrl_rot(angle):
    return TensorProduct(eye(2), do_not) + TensorProduct(rot(angle), do)


def partial_swap(angle):
    inter = ctrl_rot(angle) * ctrl_x 
    return ctrl_x * inter


def unitary_partial_swap(angles, step, n_qubits):
    inter = int(n_qubits / 2 - 1)
    if step > inter :
        raise NameError("Le qubit selectionne est incorrect.")
    elif step == 0 :
        return TensorProduct(TensorProduct(eye(2 ** (inter + step)), partial_swap(angles[inter - step])), eye(2 ** (inter - step)))
    else :
        U = TensorProduct(TensorProduct(eye(2 ** (inter + step)), partial_swap(angles[inter - step])), eye(2 ** (inter - step)))
        return TensorProduct(TensorProduct(eye(2 ** (inter - step)), partial_swap(angles[inter + step])), eye(2 ** (inter + step))) * U
    
    
def unary_circuit(angles, n_qubits):
    inter = int(n_qubits / 2 - 1)
    unary_circuit = TensorProduct(TensorProduct(eye(2 ** inter), X), eye(2 * 2 ** inter))
    for step in range(inter + 1):
        unary_circuit = unitary_partial_swap(angles, step, n_qubits) * unary_circuit
    return unary_circuit


def unary_state(angles, n_qubits):
    vec = unary_circuit(angles, n_qubits) * eye(2**n_qubits).col(0)
    unary_prob = {}
    for i in range(n_qubits):
        unary_prob[i] = vec[2 ** i] ** 2
    return unary_prob


def ratio_prob(vec):
    size = len(vec)
    ratio_prob = []
    for i in range(size - 1):
        ratio_prob.append(vec[i] / vec[i + 1])
    return ratio_prob
    


angles = {}

for i in range(n_qubits - 1):
    angles[i] = symbols('angle' + str(i + 1))
    
    
prob = unary_state(angles, n_qubits)
ratio = ratio_prob(prob)


print(prob)





