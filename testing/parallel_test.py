from time import perf_counter

from numpy import mean

from modules.parallel_solver import ParallelSolver
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from modules.utility.parameters import Parameters
from problems.gkls_function import GKLSFunction, GKLSClass
from problems.grishagin_function import GrishaginFunction
import matplotlib.pyplot as plt


def gksl(i: int):
    n = 4
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
    solver = ParallelSolver(problem, stop, param)
    solver.solve()
    sol = solver.solution
    print(f"GKLS {i}")
    print(f"Solution point: {y_opt},")
    print(f"Solution value: {z_opt},")
    print(f"My point: {sol.optimum.y},")
    print(f"My value: {sol.optimum.z},")
    print(f"Iteration count: {sol.iterationCount}")
    print("--------------------------------------")


def gkls_op():
    r = 4
    eps = 0.001
    gkls = GKLSFunction()
    gkls.SetDimension(3)
    gkls.SetFunctionClass(GKLSClass.Simple, 3)
    number_of_process = [2, 4, 8]
    plt.style.use('seaborn-v0_8')
    for n in number_of_process:
        all_iters = []
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
            if sol.optimum.z < z_opt + 9e-2:
                all_iters.append(sol.iterationCount)

            print(f"GKLS {i}")
            print(f"Solution point: {y_opt},")
            print(f"Solution value: {z_opt},")
            print(f"My point: {sol.optimum.y},")
            print(f"My value: {sol.optimum.z},")
            print(f"Accuracy: {sol.accuracy}")
            print(f"Iteration count: {sol.iterationCount}")
            print(f"Number of processes: {n}")
            print("-------------------------------------")
        acc = 0
        percent = []
        for i in range(0, max(all_iters) + 1):
            acc += all_iters.count(i)
            percent.append(acc)
        plt.plot(range(0, max(all_iters) + 1), percent, linewidth=1, label=f"{n} process")

    plt.title(f'Операционная характеристика\nПараллельная версия АГП (pool)\nФункции GKLS\nr = {r}, eps = {eps}, dim = {3}')
    plt.xlabel('Число проведённых испытаний')
    plt.ylabel('% решённых задач')
    plt.tight_layout()
    # plt.legend()
    plt.show()


def grishagin():
    k = 43
    n = 8
    grish = GrishaginFunction(k)
    y_opt = grish.GetOptimumPoint()
    z_opt = grish.Calculate(y_opt)

    problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
    stop = StopCondition(0.01, 1000)
    Parameters(2.5, n)
    solver = ParallelSolver(problem, stop)
    solver.solve()
    sol = solver.solution
    print(f"Grishagin {k}")
    print(f"Solution point: {y_opt},")
    print(f"Solution value: {z_opt},")
    print(f"My point: {sol.optimum.y},")
    print(f"My value: {sol.optimum.z},")
    print(f"Accuracy: {sol.accuracy}")
    print(f"Iteration count: {sol.iterationCount}")
    print(f"Number of processes: {n}")


def grish_op():
    r = 3
    eps = 0.001
    number_of_process = [2, 4, 8]
    plt.style.use('seaborn-v0_8')
    for n in number_of_process:
        all_iters = []
        for i in range(1, 101):
            # if i == 43 or i == 76:
            #     continue
            grish = GrishaginFunction(i)
            y_opt = grish.GetOptimumPoint()
            z_opt = grish.Calculate(y_opt)

            problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
            stop = StopCondition(eps, 10000)
            param = Parameters(r, n)
            solver = ParallelSolver(problem, stop, param)
            solver.solve()
            sol = solver.solution
            if sol.optimum.z < z_opt + 9e-2:
                all_iters.append(sol.iterationCount)

            print(f"Grishagin {i}")
            print(f"Solution point: {y_opt},")
            print(f"Solution value: {z_opt},")
            print(f"My point: {sol.optimum.y},")
            print(f"My value: {sol.optimum.z},")
            print(f"Accuracy: {sol.accuracy}")
            print(f"Iteration count: {sol.iterationCount}")
            print(f"Number of processes: {n}")
            print("-------------------------------------")
        acc = 0
        percent = []
        for i in range(0, max(all_iters)+1):
            acc += all_iters.count(i)
            percent.append(acc)
        plt.plot(range(0, max(all_iters)+1), percent, linewidth=1, label=f"{n} process")

    plt.title(f'Операционная характеристика\nПараллельная версия АГП (pool)\nФункции Гришагина\nr = {r}, eps = {eps}')
    plt.xlabel('Число проведённых испытаний')
    plt.ylabel('% решённых задач')
    plt.legend()
    plt.show()


def grish_time():
    r = 4
    eps = 0.01
    n = 8
    all_solving_time = []
    for i in range(1, 101):
        grish = GrishaginFunction(i)
        problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
        stop = StopCondition(eps, 100000)
        param = Parameters(r, n)
        solver = ParallelSolver(problem, stop, param)
        start = perf_counter()
        solver.solve()
        end = perf_counter()
        all_solving_time.append(end - start)

        print(f"Grishagin {i}")
        print(f"Solving time: {end - start} sec")
        print("-------------------------------------")
    max_solving_time = max(all_solving_time)
    avg_solving_time = mean(all_solving_time)
    print("=============================================")
    print("|\tGrishagin functions\t|")
    print("|\tParallel algorithm (pool)\t|")
    print(f"|\tr = {r}, eps = {eps}\t|")
    print(f"|\tNumber of process: {n}\t|")
    print(f"|\tMax solving time: {max_solving_time} sec\t|")
    print(f"|\tAverage solving time: {avg_solving_time} sec.\t|")
    print("=============================================")
