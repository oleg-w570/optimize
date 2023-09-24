import numpy as np

rng = np.random.RandomState()


def ShekelFunction():
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
