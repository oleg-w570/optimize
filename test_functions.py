import numpy as np

rng = np.random.RandomState()


def generateHH():
    PI = 3.1415926535897932384626433832795
    HH_COUNT = 14
    A = -1.1 + rng.rand(20) * 2.0
    B = -1.1 + rng.rand(20) * 2.0

    def HH(x):
        res = A[0]
        for i in range(1, HH_COUNT):
            res += A[i] * np.sin(i * 2 * PI * x) + B[i] * np.cos(i * 2 * PI * x)
        return res

    return HH


def generateSH():
    SH_COUNT = 10
    K = 5. + 20. * rng.rand(20)
    A = 10. * rng.rand(20)
    B = 1. + 0.2 * rng.rand(20)

    def SH(x):
        res = 0.0
        for i in range(0, SH_COUNT):
            res -= 1. / (K[i] * (x - A[i]) * (x - A[i]) + B[i])
        return res

    return SH




