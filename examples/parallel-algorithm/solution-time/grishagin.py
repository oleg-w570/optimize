from statistics import mean
from time import perf_counter

from modules.sequential_solver import SequentialSolver
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from problems.grishagin_function import GrishaginFunction


def parallel_alg_solution_time_for_grishagin(n:int, r: float, eps: float):
    solution_time = []
    for i in range(1, 101):
        grish = GrishaginFunction(i)
        problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
        stop = StopCondition(eps, 10000)
        param = Parameters(r)
        solver = SequentialSolver(problem, stop, param)
        start = perf_counter()
        solver.solve()
        end = perf_counter()
        solution_time.append(end-start)
        print(f"Grishagin {i}")
        print(f"Solving time: {end - start} sec.")
        print("-------------------------------------")
    max_solution_time = max(solution_time)
    avg_solution_time = mean(solution_time)
    print("Grishagin functions")
    print("Parallel algorithm")
    print(f"tr = {r}, eps = {eps}")
    print(f"Max solution time: {max_solution_time} sec.")
    print(f"Average solution time: {avg_solution_time} sec.")


if __name__ == "__main__":
    parallel_alg_solution_time_for_grishagin(4, 4, 0.01)
