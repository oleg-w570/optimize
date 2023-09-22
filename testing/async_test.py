from statistics import mean
from time import perf_counter

from matplotlib import pyplot as plt

from modules.async_solver import AsyncSolver
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from problems.gkls_function import GKLSClass, GKLSFunction


def all_proc_gkls_op():
    plt.style.use('seaborn-v0_8')
    num_proc = (2, 4, 8)
    r = 4
    eps = 0.01
    gkls = GKLSFunction()
    gkls.SetDimension(3)
    gkls.SetFunctionClass(GKLSClass.Simple, 3)
    for n in num_proc:
        iter_counts = []
        for i in range(1, 101):
            gkls.SetFunctionNumber(i)
            y_opt = gkls.GetOptimumPoint()
            z_opt = gkls.GetOptimumValue()
            problem = Problem(gkls.Calculate, [-1, -1, -1], [1, 1, 1], 3)
            stop = StopCondition(eps, 100000)
            param = Parameters(r, n)
            solver = AsyncSolver(problem, stop, param)
            solver.solve()
            sol = solver.solution
            iter_counts.append(sol.niter)
            # if sol.optimum.z < z_opt + 9e-2:
            #     iter_counts.append(sol.niter)

            print(f"GKLS {i}")
            print(f"Solution point: {y_opt},")
            print(f"Solution value: {z_opt},")
            print(f"My point: {sol.optimum.y},")
            print(f"My value: {sol.optimum.z},")
            print(f"Iteration count: {sol.niter}")
            print(f"Number of processes: {n}")
            print("--------------------------------------")
        acc = 0
        percent = []
        for i in range(0, max(iter_counts) + 1):
            acc += iter_counts.count(i)
            percent.append(acc)
        plt.plot(range(0, max(iter_counts) + 1), percent, linewidth=1, label=f'{n} process')
    plt.title(f'Операционная характеристика\nПараллельная асинхронная версия АГП\n'
              f'Функции GKLS\nr = {r}, eps = {eps}, dim = {3}')
    plt.xlabel('Количество итераций')
    plt.ylabel('% решённых задач')
    plt.legend()
    plt.show()


def gkls_op():
    n = 2
    r = 4
    eps = 0.01
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
        solver = AsyncSolver(problem, stop, param)
        solver.solve()
        sol = solver.solution
        if sol.optimum.z < z_opt + 9e-2:
            iter_counts.append(sol.niter)

        print(f"GKLS {i}")
        print(f"Solution point: {y_opt},")
        print(f"Solution value: {z_opt},")
        print(f"My point: {sol.optimum.y},")
        print(f"My value: {sol.optimum.z},")
        print(f"Iteration count: {sol.niter}")
        print(f"Number of processes: {n}")
        print("--------------------------------------")
    acc = 0
    percent = []
    for i in range(0, max(iter_counts) + 1):
        acc += iter_counts.count(i)
        percent.append(acc)

    plt.style.use('seaborn-v0_8')
    plt.title(f'Операционная характеристика\nПараллельная асинхронная версия АГП\n'
              f'Функции GKLS\nr = {r}, eps = {eps}, num_proc = {n}, dim = {3}')
    plt.xlabel('Число проведённых испытаний')
    plt.ylabel('% решённых задач')
    plt.plot(range(0, max(iter_counts) + 1), percent, linewidth=1, label='АГП')
    plt.legend()
    plt.show()


def gkls_time():
    n = 8
    r = 4
    eps = 0.01
    solving_time = []
    gkls = GKLSFunction()
    gkls.SetDimension(3)
    gkls.SetFunctionClass(GKLSClass.Simple, 3)
    for i in range(1, 101):
        gkls.SetFunctionNumber(i)
        problem = Problem(gkls.Calculate, [-1, -1, -1], [1, 1, 1], 3)
        stop = StopCondition(eps, 100000)
        param = Parameters(r, n)
        solver = AsyncSolver(problem, stop, param)
        # start = perf_counter()
        solver.solve()
        # end = perf_counter()
        solving_time.append(solver.solving_time)
        print(f"GKLS {i}")
        print(f"Solving time: {solver.solving_time} sec")
        print("-------------------------------------")
    max_solving_time = max(solving_time)
    avg_solving_time = mean(solving_time)
    print("GKLS functions")
    print("Asynchronous algorithm")
    print(f"r = {r}, eps = {eps}")
    print(f"Max solving time: {max_solving_time} sec")
    print(f"Average solving time: {avg_solving_time} sec.")
    print(f"Number of processes: {n}")
    

def gksl(i: int):
    n = 8
    r = 4
    eps = 0.01
    gkls = GKLSFunction()
    gkls.SetDimension(3)
    gkls.SetFunctionClass(GKLSClass.Simple, 3)
    gkls.SetFunctionNumber(i)
    y_opt = gkls.GetOptimumPoint()
    z_opt = gkls.GetOptimumValue()
    problem = Problem(gkls.Calculate, [-1, -1, -1], [1, 1, 1], 3)
    stop = StopCondition(eps, 10000)
    param = Parameters(r, n)
    solver = AsyncSolver(problem, stop, param)
    solver.solve()
    sol = solver.solution
    print(f"GKLS {i}")
    print(f"Solution point: {y_opt},")
    print(f"Solution value: {z_opt},")
    print(f"My point: {sol.optimum.y},")
    print(f"My value: {sol.optimum.z},")
    print(f"Iteration count: {sol.niter}")
    print(f"Solving time: {solver.solving_time}")
    print("--------------------------------------")