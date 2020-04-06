from math import pi


def format_angle(angle, error, desired_precision):
    q = 0
    for i in range(desired_precision):
        i = i + 1
        if ((i * angle) % pi) < error:
            q = i
            break
    if q == 0:
        return str(angle)
    else:
        str_p = ''
        str_q = ''
        p = round((q * angle) / pi)
        if p != 1:
            str_p = str(p)
        if q != 1:
            str_q = '/' + str(q)
        return '$' + str_p + '\pi' + str_q + '$'