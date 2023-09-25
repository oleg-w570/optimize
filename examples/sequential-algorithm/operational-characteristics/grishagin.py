from matplotlib import pyplot as plt

from modules.solve import solve
from problems.grishagin.grishagin import Grishagin


if __name__ == "__main__":
    r = 4
    eps = 0.01
    plt.style.use('seaborn-v0_8')
    iter_counts = []
    for i in range(1, 101):
        problem = Grishagin(i)
        print(problem)
        sol = solve(problem,
                    r=r, eps=eps,
                    alg='seq')
        print(sol)
        iter_counts.append(sol.niter)
        # if sol.optimum.z < z_opt + 9e-2:
        #     iter_counts.append(sol.niter)
        print("--------------------------------------")
    acc = 0
    percent = []
    for i in range(0, max(iter_counts) + 1):
        acc += iter_counts.count(i)
        percent.append(acc)
    plt.title(f'Операционная характеристика\nПоследовательная версия АГП\n'
              f'Функции Гришагина\nr = {r}, eps = {eps}')
    plt.xlabel('Количество итераций')
    plt.ylabel('% решённых задач')
    plt.plot(range(0, max(iter_counts) + 1), percent, linewidth=1, label='АГП')
    plt.legend()
    plt.show()
