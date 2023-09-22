from modules.parallel_solver import ParallelSolver
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from problems.grishagin_function import GrishaginFunction


def parallel_alg_grishagin(i: int, n:int, r: float, eps: float):
    grish = GrishaginFunction(i)
    y_opt = grish.GetOptimumPoint()
    z_opt = grish.Calculate(y_opt)
    problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
    stop = StopCondition(eps, 100000)
    param = Parameters(r)
    solver = ParallelSolver(problem, stop, param)
    solver.solve()
    sol = solver.solution
    print(f"Grishagin {i}")
    print(f"Solution point: {y_opt},")
    print(f"Solution value: {z_opt},")
    print(f"Calculated point: {sol.optimumPoint},")
    print(f"Calculated value: {sol.optimumValue},")
    print(f"Iteration count: {sol.niter}")


if __name__ == "__main__":
    parallel_alg_grishagin(31, 4, 4, 0.01)
