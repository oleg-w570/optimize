from time import perf_counter

from matplotlib import pyplot as plt
from mpi4py import MPI
from numpy import mean

from modules.mpisolver import MPISolver
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from problems.grishagin_function import GrishaginFunction
from problems.gkls_function import GKLSFunction, GKLSClass


def grish_time():
    rank = MPI.COMM_WORLD.rank
    r = 4
    eps = 0.01
    if rank == 0:
        all_solving_time = []
    for i in range(1, 101):
        grish = GrishaginFunction(i)
        problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
        stop = StopCondition(eps, 100000)
        param = Parameters(r)
        solver = MPISolver(problem, stop, param)
        if rank == 0:
            start = perf_counter()
        solver.solve()
        if rank == 0:
            end = perf_counter()
            all_solving_time.append(end - start)
            # print(f"Grishagin {i}")
            # print(f"Solving time: {end - start} sec")
            # print(f"-------------------------------------")
    if rank == 0:
        max_solving_time = max(all_solving_time)
        avg_solving_time = mean(all_solving_time)
        print("============================================================")
        print("|\tGrishagin functions\t|")
        print("|\tParallel algorithm (mpi)\t|")
        print(f"|\tr = {r}, eps = {eps}\t|")
        print(f"|\tNumber of process: mpi={MPI.COMM_WORLD.size}\t|")
        print(f"|\tMax solving time: {max_solving_time} sec\t|")
        print(f"|\tAverage solving time: {avg_solving_time} sec.\t|")
        print("============================================================")


def grish_op():
    r = 3
    eps = 0.001
    rank = MPI.COMM_WORLD.rank
    plt.style.use('seaborn-v0_8')
    if rank == 0:
        allIters = []
    for i in range(1, 101):
        grish = GrishaginFunction(i)
        if rank == 0:
            y_opt = grish.GetOptimumPoint()
            z_opt = grish.Calculate(y_opt)
        problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
        stop = StopCondition(eps, 10000)
        param = Parameters(r)
        solver = MPISolver(problem, stop, param)
        solver.solve()
        if rank == 0:
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
            print(f"Number of processes: {MPI.COMM_WORLD.size}")
            print("-------------------------------------")
    if rank == 0:
        acc = 0
        percent = []
        for i in range(0, max(allIters)+1):
            acc += allIters.count(i)
            percent.append(acc)
        plt.plot(range(0, max(allIters)+1), percent, linewidth=1)
        plt.title(f'Операционная характеристика\nПараллельная версия АГП (MPI)\nФункции Гришагина\n'
                  f'r = {r}, eps = {eps}, mpi_size = {MPI.COMM_WORLD.size}')
        plt.xlabel('Число проведённых испытаний')
        plt.ylabel('% решённых задач')
        plt.legend()
        plt.show()

def gkls(i: int):
    rank = MPI.COMM_WORLD.rank
    r = 3
    eps = 0.01
    gkls = GKLSFunction()
    gkls.SetDimension(3)
    gkls.SetFunctionClass(GKLSClass.Simple, 3)
    gkls.SetFunctionNumber(i)
    if rank == 0:
        y_opt = gkls.GetOptimumPoint()
        z_opt = gkls.GetOptimumValue()
    problem = Problem(gkls.Calculate, [-1, -1, -1], [1, 1, 1], 3)
    stop = StopCondition(eps, 10000)
    param = Parameters(r)
    solver = MPISolver(problem, stop, param)
    solver.solve()
    if rank == 0:
        sol = solver.solution
        print(f"GKLS {i}")
        print(f"Solution point: {y_opt},")
        print(f"Solution value: {z_opt},")
        print(f"My point: {sol.optimum.y},")
        print(f"My value: {sol.optimum.z},")
        print(f"Iteration count: {sol.iterationCount}")
        print(f"MPI Process: {MPI.COMM_WORLD.size}")
        print("--------------------------------------")

def gkls_time():
    rank = MPI.COMM_WORLD.rank
    r = 4
    eps = 0.01
    gkls = GKLSFunction()
    gkls.SetDimension(3)
    gkls.SetFunctionClass(GKLSClass.Simple, 3)
    if rank == 0:
        all_solving_time = []
    for i in range(1, 101):
        gkls.SetFunctionNumber(i)
        problem = Problem(gkls.Calculate, [-1, -1, -1], [1, 1, 1], 3)
        stop = StopCondition(eps, 100000)
        param = Parameters(r)
        solver = MPISolver(problem, stop, param)
        if rank == 0:
            start = perf_counter()
        solver.solve()
        if rank == 0:
            end = perf_counter()
            all_solving_time.append(end - start)
            # print(f"Grishagin {i}")
            # print(f"Solving time: {end - start} sec")
            # print(f"-------------------------------------")
    if rank == 0:
        max_solving_time = max(all_solving_time)
        avg_solving_time = mean(all_solving_time)
        print("============================================================")
        print("|\tGKLS functions\t|")
        print("|\tParallel algorithm (mpi)\t|")
        print(f"|\tr = {r}, eps = {eps}\t|")
        print(f"|\tNumber of process: mpi={MPI.COMM_WORLD.size}\t|")
        print(f"|\tMax solving time: {max_solving_time} sec\t|")
        print(f"|\tAverage solving time: {avg_solving_time} sec.\t|")
        print("============================================================")

def grishagin(k: int):
    grish = GrishaginFunction(k)
    y_opt = grish.GetOptimumPoint()
    z_opt = grish.Calculate(y_opt)

    problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
    stop = StopCondition(0.01, 10000)
    param = Parameters(2.5)
    solver = MPISolver(problem, stop, param)
    solver.solve()

    if MPI.COMM_WORLD.rank == 0:
        sol = solver.solution
        print(f"Grishagin {k}")
        print(f"Solution point: {y_opt},")
        print(f"Solution value: {z_opt},")
        print(f"My point: {sol.optimum.y},")
        print(f"My value: {sol.optimum.z},")
        print(f"Accuracy: {sol.accuracy}")
        print(f"Iteration count: {sol.iterationCount}")