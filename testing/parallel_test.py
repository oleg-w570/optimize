from datetime import datetime
from modules.core.parallelsolver import ParallelSolver
from modules.core.sequentialsolver import SequentialSolver
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from modules.utility.parameters import Parameters
from problems.grishagin_function import GrishaginFunction
from problems.hill_function import HillFunction

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(10000)

def TestGrish():
    # k = random.randint(1, 100)
    k = 43
    grish = GrishaginFunction(k)
    y_opt = grish.GetOptimumPoint()
    z_opt = grish.Calculate(y_opt)

    problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
    stop = StopCondition(0.01, 1000)
    solver = SequentialSolver(problem, stop)
    solver.solve()
    sol = solver.solution
    print(f"Grishagin {k}")
    print(f"Solution point: {y_opt},")
    print(f"Solution value: {z_opt},")
    print(f"My point: {sol.optimum.y},")
    print(f"My value: {sol.optimum.z},")
    print(f"Accuracy: {sol.accuracy}")
    print(f"Iteration count: {sol.iterationCount}")

def TestParallel():
    # k = random.randint(1, 100)
    k = 43
    grish = GrishaginFunction(k)
    y_opt = grish.GetOptimumPoint()
    z_opt = grish.Calculate(y_opt)

    problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
    stop = StopCondition(0.01, 1000)
    param = Parameters(2.5, 1)
    solver = ParallelSolver(problem, stop, param)
    solver.solve()
    sol = solver.solution
    print(f"Grishagin {k}")
    print(f"Solution point: {y_opt},")
    print(f"Solution value: {z_opt},")
    print(f"My point: {sol.optimum.y},")
    print(f"My value: {sol.optimum.z},")
    print(f"Accuracy: {sol.accuracy}")
    print(f"Iteration count: {sol.iterationCount}")

def ParallelOp():
    r = 4
    eps = 0.01
    numberOfProcess = [1, 2, 4, 8]
    plt.style.use('seaborn-v0_8')
    for n in numberOfProcess:
        allIters = []
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
                allIters.append(sol.iterationCount)

            print(f"Grishagin {i}")
            print(f"Solution point: {y_opt},")
            print(f"Solution value: {z_opt},")
            print(f"My point: {sol.optimum.y},")
            print(f"My value: {sol.optimum.z},")
            print(f"Accuracy: {sol.accuracy}")
            print(f"Iteration count: {sol.iterationCount}")
            print(f"Number of processes: {n}")
            print(f"-------------------------------------")
        acc = 0
        percent = []
        for i in range(0, max(allIters)+1):
            acc += allIters.count(i)
            percent.append(acc)
        plt.plot(range(0, max(allIters)+1), percent, linewidth=1, label=f"{n} process")

    plt.title(f'Операционная характеристика параллельной версии АГП\nфункции Гришагина\nr = {r}, eps = {eps}')
    plt.xlabel('Число проведённых испытаний')
    plt.ylabel('% решённых задач')
    plt.legend()
    plt.show()

def SolvingTime():
    r = 3
    eps = 0.01
    n = 8
    allSolvingTime = 0
    for i in range(10, 11):
        grish = GrishaginFunction(i)
        y_opt = grish.GetOptimumPoint()
        z_opt = grish.Calculate(y_opt)

        problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
        stop = StopCondition(eps, 10000)
        param = Parameters(r, n)
        solver = ParallelSolver(problem, stop, param)
        startTime = datetime.now()
        solver.solve()
        solvingTime = (datetime.now() - startTime).total_seconds()
        allSolvingTime += solvingTime
        sol = solver.solution

        print(f"Grishagin {i}")
        print(f"Solution point: {y_opt},")
        print(f"Solution value: {z_opt},")
        print(f"My point: {sol.optimum.y},")
        print(f"My value: {sol.optimum.z},")
        print(f"Accuracy: {sol.accuracy},")
        print(f"Iteration count: {sol.iterationCount},")
        print(f"Solving time: {solvingTime} sec,")
        print(f"Number of processes: {n}")
        print(f"-------------------------------------")
    avgSolvingTime = allSolvingTime / 100
    print(f"Average solving time: {avgSolvingTime} sec.")
