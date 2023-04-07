import numpy as np
import matplotlib.pyplot as plt
from archive.agp_third import AGP
from problems.hill_function import HillFunction
from report.for_report import agp_op
from report.for_report_jmetal import jmetal_op
from archive.agp_first import AGP

def agp_on_graph():
    f = HillFunction()
    algorithm = AGP(f, 0, 1, 2.5)  # SH: b = 10, HH: b = 1
    algorithm.run()
    x_test, y_test, niter = algorithm.get_result()
    y_min = min(y_test)
    x_min = x_test[y_test.index(y_min)]

    x = np.linspace(0, 1, 200)  # SH: stop = 10, HH: stop = 1
    y = list(map(f, x))

    plt.style.use('seaborn-v0_8')
    plt.plot(x, y, linewidth=1, label='функция')
    plt.scatter(x_test, y_test, marker='|', c='green', label='точки испытаний')
    plt.scatter(x_min, y_min, s=30, c='black', label='точка минимума')
    plt.legend()
    plt.show()


N = 1000
test_func_class_name = 'SH'
r = 2.5
eps = 1e-3
agp_percent, max_niter = agp_op(test_func_class_name, eps, N, r)
jmetal_percent = jmetal_op(test_func_class_name, max_niter, eps, 50, 1)
x1 = np.arange(0, max_niter)
# x2 = np.arange(0, max_k)
y1 = agp_percent
y2 = jmetal_percent
plt.style.use('seaborn-v0_8')
plt.title('Операционные характеристики функции Шекеля')
plt.xlabel('Число проведённых испытаний')
plt.ylabel('% решённых задач')
plt.plot(x1, y1, linewidth=1, label='АГП')
plt.plot(x1, y2, linewidth=1, label='Эвристический метод jMetal')
plt.legend()
plt.show()
