from matplotlib import pyplot as plt

from modules.parallel_solver import ParallelSolver
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from problems.grishagin_function import GrishaginFunction


def parallel_alg_operational_characteristic_for_grishagin(n:int, r: float, eps: float):
    plt.style.use('seaborn-v0_8')
    iter_counts = []
    for i in range(1, 101):
        grish = GrishaginFunction(i)
        y_opt = grish.GetOptimumPoint()
        z_opt = grish.Calculate(y_opt)
        problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
        stop = StopCondition(eps, 10000)
        param = Parameters(r, n)
        solver = ParallelSolver(problem, stop, param)
        solver.solve()
        sol = solver.solution
        iter_counts.append(sol.niter)
        # if sol.optimum.z < z_opt + 9e-2:
        #     iter_counts.append(sol.niter)
        print(f"GKLS {i}")
        print(f"Solution point: {y_opt},")
        print(f"Solution value: {z_opt},")
        print(f"Calculated point: {sol.optimum.y},")
        print(f"Calculated value: {sol.optimum.z},")
        print(f"Iteration count: {sol.niter}")
        print("--------------------------------------")
    acc = 0
    percent = []
    for i in range(0, max(iter_counts) + 1):
        acc += iter_counts.count(i)
        percent.append(acc)
    plt.title(f'Операционная характеристика\nПараллельная версия АГП\n'
              f'Функции Гришагина\nr = {r}, eps = {eps}, num_proc = {n}')
    plt.xlabel('Число проведённых испытаний')
    plt.ylabel('% решённых задач')
    plt.plot(range(0, max(iter_counts) + 1), percent, linewidth=1, label='АГП')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    parallel_alg_operational_characteristic_for_grishagin(4, 4, 0.01)