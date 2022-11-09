import numpy as np
import matplotlib.pyplot as plt
import methods as mthd
import test_functions as func

# f = func.HH
f = func.SH
x_test, y_test = mthd.AGP(f, 0, 10, 2.5)  # SH: b = 10, HH: b = 1
y_min = min(y_test)
x_min = x_test[y_test.index(y_min)]

x = np.linspace(0, 10, 200)  # SH: stop = 10, HH: stop = 1
y = list(map(f, x))

plt.style.use('seaborn-v0_8')
plt.plot(x, y, linewidth=1, label='функция')
plt.scatter(x_test, y_test, marker='|', c='green', label='точки испытаний')
plt.scatter(x_min, y_min, s=30, c='black', label='точка минимума')
plt.legend()
plt.show()
