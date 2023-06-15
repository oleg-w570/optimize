from archive.agp_third import AGP
from problems.hill_function import HillFunction
from problems.shekel_function import ShekelFunction
import numpy as np


# N = 1000
# eps = 1e-4
# r = 2.5
# right_border = 1
def agp_op(test_func_class, eps, N, r):
    total_niter = []
    # total_k = []
    right_border = 1 if test_func_class == 'HL' else 10
    for i in range(0, N):
        f = HillFunction() if test_func_class == 'HL' else ShekelFunction()
        # решение методом перебора
        minimum = min(map(f, np.arange(0, right_border, eps)))
        # решение с помощью АГП
        # wtf, k = AAA.AGP(f, 0, right_border, r, eps)
        algorithm = AGP(f, 0, right_border, r, eps)
        algorithm.run()
        _, y, niter = algorithm.get_result()
        # if wtf < minimum + 1e-2:
        #     total_k.append(k)
        if min(y) < minimum + 1e-2:
            total_niter.append(niter)
        else:
            print("Неверное решение на", i, "итерации! Правильно:", minimum, "\tимеем:", min(y))

    max_niter = max(total_niter)
    percent_niter = []
    acc = 0
    for i in range(0, max_niter):
        acc += total_niter.count(i)
        percent_niter.append(acc / N * 100)
    # max_k = max(total_k)
    # percent_k = []
    # acc = 0
    # for i in range(0, max_k):
    #     acc += total_k.count(i)
    #     percent_k.append(acc / N * 100)
    return percent_niter, max_niter#, percent_k, max_k


# x1 = np.arange(0, max_niter)
# y1 = percent_niter
# plt.style.use('seaborn-v0_8')
# plt.title('Операционная характеристика АГП\nФункции из класса HH\nr = {0}, eps = {1}'.format(r, eps))
# plt.xlabel('Число итераций')
# plt.ylabel('% решённых задач')
# plt.plot(x1, y1, linewidth=1)
# plt.legend()
# plt.show()
