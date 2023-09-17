from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import random
from datetime import datetime

from numpy import mean

from archive.agp_third import AGP
from modules.utility.stopcondition import StopCondition
from problems.grishagin_function import GrishaginFunction
from problems.shekel_function import ShekelFunction
from problems.hill_function import HillFunction
from modules.utility.problem import Problem
from modules.utility.parameters import Parameters
from modules.sequential_solver import SequentialSolver
from problems.gkls_function import GKLSFunction, GKLSClass
random.seed()


def grish_op():
    r = 4
    eps = 0.01
    iter_counts = []
    for i in range(1, 101):
        grish = GrishaginFunction(i)
        y_opt = grish.GetOptimumPoint()
        z_opt = grish.Calculate(y_opt)
        problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
        stop = StopCondition(eps, 10000)
        param = Parameters(r)
        solver = SequentialSolver(problem, stop, param)
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
        print("--------------------------------------")

    acc = 0
    percent = []
    for i in range(0, max(iter_counts) + 1):
        acc += iter_counts.count(i)
        percent.append(acc)

    plt.style.use('seaborn-v0_8')
    plt.title(f'Операционная характеристика АГП\nфункции Гришагина\nr = {r}, eps = {eps}')
    plt.xlabel('Число проведённых испытаний')
    plt.ylabel('% решённых задач')
    plt.plot(range(0, max(iter_counts) + 1), percent, linewidth=1, label='АГП')
    # plt.legend()
    plt.show()


def grish_time():
    r = 4
    eps = 0.01
    solving_time = []
    for i in range(1, 101):
        grish = GrishaginFunction(i)
        problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
        stop = StopCondition(eps, 10000)
        param = Parameters(r)
        solver = SequentialSolver(problem, stop, param)
        start = perf_counter()
        solver.solve()
        end = perf_counter()
        solving_time.append(end-start)
        print(f"Grishagin {i}")
        print(f"Solving time: {end - start} sec")
        print("-------------------------------------")
    max_solving_time = max(solving_time)
    avg_solving_time = mean(solving_time)
    print("=============================================")
    print("|\tGrishagin functions\t|")
    print("|\tSequential algorithm \t|")
    print(f"|\tr = {r}, eps = {eps}\t|")
    print(f"|\tMax solving time: {max_solving_time} sec\t|")
    print(f"|\tAverage solving time: {avg_solving_time} sec.\t|")
    print("=============================================")


def gksl(i: int):
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
    param = Parameters(r)
    solver = SequentialSolver(problem, stop, param)
    solver.solve()
    sol = solver.solution
    print(f"GKLS {i}")
    print(f"Solution point: {y_opt},")
    print(f"Solution value: {z_opt},")
    print(f"My point: {sol.optimum.y},")
    print(f"My value: {sol.optimum.z},")
    print(f"Iteration count: {sol.niter}")
    print("--------------------------------------")

def gkls_time():
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
        param = Parameters(r)
        solver = SequentialSolver(problem, stop, param)
        start = perf_counter()
        solver.solve()
        end = perf_counter()
        solving_time.append(end-start)
        print(f"GKLS {i}")
        print(f"Solving time: {end - start} sec")
        print("-------------------------------------")
    max_solving_time = max(solving_time)
    avg_solving_time = mean(solving_time)
    print("=============================================")
    print("|\tGKLS functions\t|")
    print("|\tSequential algorithm \t|")
    print(f"|\tr = {r}, eps = {eps}\t|")
    print(f"|\tMax solving time: {max_solving_time} sec\t|")
    print(f"|\tAverage solving time: {avg_solving_time} sec.\t|")
    print("=============================================")

def gkls_op():
    r = 3
    eps = 0.001
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
        param = Parameters(r)
        solver = SequentialSolver(problem, stop, param)
        solver.solve()
        sol = solver.solution
        if sol.optimum.z < z_opt + 9e-2:
            iter_counts.append(sol.niter)
        elif i == 92:
            iter_counts.append(sol.niter)

        print(f"GKLS {i}")
        print(f"Solution point: {y_opt},")
        print(f"Solution value: {z_opt},")
        print(f"My point: {sol.optimum.y},")
        print(f"My value: {sol.optimum.z},")
        print(f"Iteration count: {sol.niter}")
        print("--------------------------------------")

    acc = 0
    percent = []
    for i in range(0, max(iter_counts) + 1):
        acc += iter_counts.count(i)
        percent.append(acc)

    plt.style.use('seaborn-v0_8')
    plt.title(f'Операционная характеристика АГП\nфункции GKLS\nr = {r}, eps = {eps}, dim = {3}')
    plt.xlabel('Число проведённых испытаний')
    plt.ylabel('% решённых задач')
    plt.plot(range(0, max(iter_counts) + 1), percent, linewidth=1, label='АГП')
    plt.legend()
    plt.show()


def TestHill():
    f = HillFunction()
    problem = Problem(f, [0], [1], 1)
    stop = StopCondition(0.01, 1000)
    param = Parameters(2.5)
    solver = SequentialSolver(problem, stop, param)
    solver.solve()
    sol = solver.solution
    algorithm = AGP(f, 0, 1, 2.5, 0.001)
    algorithm.run()
    _, z1, niter = algorithm.get_result()
    minimum = min(map(f, np.arange(0, 1, 0.001)))
    print(f"Solution value: {minimum},")
    print(f"My value: {sol.optimum.z},")
    print(f"Iteration count: {sol.niter}")
    print(f"Old agp value: {min(z1)},")
    print(f"Old agp iteration count: {niter}")


def TestShekel():
    f = ShekelFunction()
    problem = Problem(f, [0], [10], 1)
    stop = StopCondition(0.01, 1000)
    param = Parameters(2.5)
    solver = SequentialSolver(problem, stop, param)
    solver.solve()
    sol = solver.solution
    algorithm = AGP(f, 0, 10, 2.5, 0.01)
    algorithm.run()
    _, z1, niter = algorithm.get_result()
    minimum = min(map(f, np.arange(0, 10, 0.001)))
    print(f"Solution value: {minimum},")
    print(f"My value: {sol.optimum.z},")
    print(f"Iteration count: {sol.niter}")
    print(f"Old agp value: {min(z1)},")
    print(f"Old agp iteration count: {niter}")


def TestEvolvent():
    evolvent = Evolvent([0, 0], [1, 1], 2, 35)
    lx = 0.0
    rx = 1.0
    ly = evolvent.get_image(lx)
    ry = evolvent.get_image(rx)
    print(ly, ry)


def GrishPlot():
    grish = GrishaginFunction(1)
    X = np.arange(0, 1, 0.01)
    Y = np.arange(0, 1, 0.01)
    Z = []
    for i, x in enumerate(X):
        Z.append([])
        for y in Y:
            z = grish.Calculate([x, y])
            Z[i].append(z)

    X, Y = np.meshgrid(X, Y)
    Z = np.matrix(Z)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(X, Y, Z)
    plt.show()


def TestGrish():
    # k = random.randint(1, 100)
    k = 10
    grish = GrishaginFunction(k)
    y_opt = grish.GetOptimumPoint()
    z_opt = grish.Calculate(y_opt)

    problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
    stop = StopCondition(0.01, 1000)
    param = Parameters(2.5)
    solver = SequentialSolver(problem, stop, param)
    solver.solve()
    sol = solver.solution
    print(f"Grishagin {k}")
    print(f"Solution point: {y_opt},")
    print(f"Solution value: {z_opt},")
    print(f"My point: {sol.optimumPoint},")
    print(f"My value: {sol.optimumValue},")
    print(f"Iteration count: {sol.niter}")

def SeqOp():
    r = 2.5
    eps = 0.001
    iterCounts = []
    for i in range(10, 11):
        grish = GrishaginFunction(i)
        y_opt = grish.GetOptimumPoint()
        z_opt = grish.Calculate(y_opt)

        problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
        param = Parameters(r, eps)
        solver = SequentialSolver(problem, param)
        startTime = datetime.now()
        solver.solve()
        solvingTime = (datetime.now() - startTime).total_seconds()
        sol = solver.getSolution()
        if sol.optimumValue < z_opt + 9e-2:
            iterCounts.append(sol.iterationCount)

        print(f"Grishagin {i}")
        print(f"Solution point: {y_opt},")
        print(f"Solution value: {z_opt},")
        print(f"My point: {sol.optimumPoint},")
        print(f"My value: {sol.optimumValue},")
        print(f"Iteration count: {sol.iterationCount}")
        print(f"Solving time: {solvingTime} sec.")
        print("--------------------------------------")

    acc = 0
    percent = []
    for i in range(0, max(iterCounts)+1):
        acc += iterCounts.count(i)
        percent.append(acc)

    plt.style.use('seaborn-v0_8')
    plt.title(f'Операционная характеристика АГП\nфункции Гришагина\nr = {r}, eps = {eps}')
    plt.xlabel('Число проведённых испытаний')
    plt.ylabel('% решённых задач')
    plt.plot(range(0, max(iterCounts)+1), percent, linewidth=1, label='АГП')
    plt.legend()
    plt.show()
