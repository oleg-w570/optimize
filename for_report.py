from agp import AGP
from test_functions import generateHH, generateSH
import numpy as np
import matplotlib.pyplot as plt

total_niter = []
N = 10000
for i in range(0, N):
    f = generateHH()
    algorithm = AGP(f, 0, 1, 3)
    algorithm.run()
    niter = algorithm.get_result()[2]
    total_niter.append(niter)
# print(total_niter)
max_niter = max(total_niter)
percent_iter = []
border = 0
step = 1
tmp = 0
while border < max_niter:
    tmp += len(list(filter(lambda it: border <= it < border + step, total_niter)))
    percent_iter.append(tmp/N * 100)
    border += step
# print(percent_iter)

x1 = np.arange(0, max_niter, step)
y1 = percent_iter
plt.style.use('seaborn-v0_8')
plt.title('Операционная характеристика АГП')
plt.xlabel('Число итераций')
plt.ylabel('% решённых задач')
plt.plot(x1, y1, linewidth=1)
plt.legend()
plt.show()
