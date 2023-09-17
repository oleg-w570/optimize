from statistics import mean

from modules.async_solver import AsyncSolver
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from problems.gkls_function import GKLSClass, GKLSFunction


def gkls_time():
    n = 4
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
    print("=============================================")
    print("|\tGKLS functions\t|")
    print("|\tSequential algorithm \t|")
    print(f"|\tr = {r}, eps = {eps}\t|")
    print(f"|\tMax solving time: {max_solving_time} sec\t|")
    print(f"|\tAverage solving time: {avg_solving_time} sec.\t|")
    print(f"Number of processes: {n}")
    print("=============================================")
    

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
    print("--------------------------------------")