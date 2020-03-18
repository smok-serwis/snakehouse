cdef extern from "test_n.h":
    float _times_five(float)


def times_five(x):
    return _times_five(x)

def times_three(x):
    return x*3
