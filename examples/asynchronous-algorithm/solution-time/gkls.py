from statistics import mean
from time import perf_counter

from modules.async_solver import AsyncSolver
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from problems.gkls_function import GKLSFunction, GKLSClass


def async_alg_solution_time_for_gkls(n: int, r: float, eps: float):
    solution_time = []
    gkls = GKLSFunction()
    gkls.SetDimension(3)
    gkls.SetFunctionClass(GKLSClass.Simple, 3)
    for i in range(1, 101):
        gkls.SetFunctionNumber(i)
        problem = Problem(gkls.Calculate, [-1, -1, -1], [1, 1, 1], 3)
        stop = StopCondition(eps, 100000)
        param = Parameters(r)
        solver = AsyncSolver(problem, stop, param)
        start = perf_counter()
        solver.solve()
        end = perf_counter()
        solution_time.append(end-start)
        print(f"GKLS {i}")
        print(f"Solving time: {end - start} sec.")
        print("-------------------------------------")
    max_solution_time = max(solution_time)
    avg_solution_time = mean(solution_time)
    print("GKLS functions")
    print("Asynchronous algorithm")
    print(f"r = {r}, eps = {eps}")
    print(f"Max solving time: {max_solution_time} sec.")
    print(f"Average solving time: {avg_solution_time} sec.")


if __name__ == "__main__":
    async_alg_solution_time_for_gkls(4, 4, 0.01)
