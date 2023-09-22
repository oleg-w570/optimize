from matplotlib import pyplot as plt

from modules.parallel_solver import ParallelSolver
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from problems.gkls_function import GKLSFunction, GKLSClass


def parallel_alg_operational_characteristic_for_gkls(n: int, r: float, eps: float):
    plt.style.use('seaborn-v0_8')
    iter_counts = []
    gkls = GKLSFunction()
    gkls.SetDimension(3)
    gkls.SetFunctionClass(GKLSClass.Simple, 3)
    for i in range(1, 101):
        gkls.SetFunctionNumber(i)
        y_opt = gkls.GetOptimumPoint()
        z_opt = gkls.GetOptimumValue()
        problem = Problem(gkls.Calculate, [-1, -1, -1], [1, 1, 1], 3)
        stop = StopCondition(eps, 100000)
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
    plt.title(f'Операционная характеристика\nПараллельная версия АГП'
              f'\nФункции GKLS\nr = {r}, eps = {eps}, num_proc = {n}, dim = {3}')
    plt.xlabel('Количество итераций')
    plt.ylabel('% решённых задач')
    plt.plot(range(0, max(iter_counts) + 1), percent, linewidth=1, label='АГП')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    parallel_alg_operational_characteristic_for_gkls(4, 4, 0.01)