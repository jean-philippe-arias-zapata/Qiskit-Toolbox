def to_list(x):
    if type(x) == float or type(x) == int:
        x = [x]
    return x


def is_boolean_list(x):
    is_boolean = True
    if type(x) == list:
        for i in range(len(x)):
            if x[i] != 0 and x[i] != 1:
                is_boolean = False
                break
        return is_boolean
    else:
        raise NameError("The input is not a list.")