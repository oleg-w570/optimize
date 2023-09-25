import numpy as np

rng = np.random.RandomState()


def HillFunction():
    PI = 3.1415926535897932384626433832795
    HH_COUNT = 14
    A = -1.1 + rng.rand(20) * 2.0
    B = -1.1 + rng.rand(20) * 2.0

    def HL(x):
        res = A[0]
        for i in range(1, HH_COUNT):
            res += A[i] * np.sin(i * 2 * PI * x) + B[i] * np.cos(i * 2 * PI * x)
        return res

    return HL
