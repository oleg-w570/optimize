import matplotlib.pyplot as plt
import numpy as np
import random
from archive.agp_third import AGP
from problems.grishagin_function import GrishaginFunction
from problems.shekel_function import ShekelFunction
from problems.hill_function import HillFunction
from modules.utility.problem import Problem
from modules.utility.parameters import Parameters
from modules.utility.interval import IntervalData
from modules.core.evolvent import Evolvent
from modules.core.solver import Solver

random.seed()

def TestHill():
    f = HillFunction()
    problem = Problem(f, [0], [1], 1)
    param = Parameters(2.5, 0.001)
    sol = Solver(problem, param)
    sol.solve()
    algorithm = AGP(f, 0, 1, 2.5, 0.001)
    algorithm.run()
    _, z1, niter = algorithm.get_result()
    minimum = min(map(f, np.arange(0, 1, 0.001)))
    print(f"Solution value: {minimum},")
    print(f"My value: {sol.z_opt},")
    print(f"Iteration count: {sol.iterationCount}")
    print(f"Old agp value: {min(z1)},")
    print(f"Old agp iteration count: {niter}")

def TestShekel():
    f = ShekelFunction()
    problem = Problem(f, [0], [10], 1)
    param = Parameters(2.5, 0.01)
    sol = Solver(problem, param)
    sol.solve()
    algorithm = AGP(f, 0, 10, 2.5, 0.01)
    algorithm.run()
    _, z1, niter = algorithm.get_result()
    minimum = min(map(f, np.arange(0, 10, 0.001)))
    print(f"Solution value: {minimum},")
    print(f"My value: {sol.z_opt},")
    print(f"Iteration count: {sol.iterationCount}")
    print(f"Old agp value: {min(z1)},")
    print(f"Old agp iteration count: {niter}")

def TestGrish():
    k = random.randint(1, 100)
    grish = GrishaginFunction(k)
    y_opt = grish.GetOptimumPoint()
    z_opt = grish.Calculate(y_opt)

    problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
    param = Parameters(2.5, 0.001)
    sol = Solver(problem, param)
    sol.solve()
    print(f"Grishagin {k}")
    print(f"Solution point: {y_opt},")
    print(f"Solution value: {z_opt},")
    print(f"My value: {sol.z_opt},")
    print(f"Iteration count: {sol.iterationCount}")

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

if __name__ == "__main__":
    TestGrish()
