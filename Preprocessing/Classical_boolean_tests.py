import numpy as np
from Classical_data_preparation import lineic_preprocessing


def is_stochastic_vector(distribution): #is the given array a stochastic vector ? Must be normalized (norm 1)
    distribution = np.array(distribution)
    size = distribution.size
    distribution = lineic_preprocessing(distribution, vertical=False)
    is_stochastic_vector = False
    is_normalized = False
    is_positive = True
    if np.isclose(sum(distribution), 1, atol=1e-04):
        is_normalized = True
    for i in range(size):
        if distribution[i] < 0:
            is_positive = False
    if is_normalized == True and is_positive == True:
        is_stochastic_vector = True
    return is_stochastic_vector


def is_log_concave(distribution): #is the given array a log-concave stochastic vector ?
    something = True #have to define what condition must respect a log-concave distribution
    is_log_concave = False
    if is_stochastic_vector(distribution) == True and something == True:
        is_log_concave = True
    return is_log_concave
    

def is_log_concave_encoding_compatible(distribution, n_qubits): #is the given array an n_qubits-implementable log-concave distribution ?
    is_compatible = False
    distribution = np.array(distribution)
    if is_log_concave(distribution) == True and distribution.size % 2**(n_qubits) == 0:
        is_compatible = True
    return is_compatible
    