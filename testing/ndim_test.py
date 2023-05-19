import matplotlib.pyplot as plt
import numpy as np
import random
from datetime import datetime
from archive.agp_third import AGP
from modules.utility.stopcondition import StopCondition
from problems.grishagin_function import GrishaginFunction
from problems.shekel_function import ShekelFunction
from problems.hill_function import HillFunction
from modules.utility.problem import Problem
from modules.utility.parameters import Parameters
from modules.core.evolvent import Evolvent
from modules.core.sequentialsolver import SequentialSolver

random.seed()

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
    print(f"Iteration count: {sol.iterationCount}")
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
    print(f"Iteration count: {sol.iterationCount}")
    print(f"Old agp value: {min(z1)},")
    print(f"Old agp iteration count: {niter}")


def TestEvolvent():
    evolvent = Evolvent([0, 0], [1, 1], 2, 35)
    lx = 0.0
    rx = 1.0
    ly = evolvent.GetImage(lx)
    ry = evolvent.GetImage(rx)
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
    print(f"Iteration count: {sol.iterationCount}")

def SeqOp():
    r = 4
    eps = 0.01
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
