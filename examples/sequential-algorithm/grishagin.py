from modules.sequential_solver import SequentialSolver
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from problems.grishagin_function import GrishaginFunction


def seq_alg_grishagin(i: int, r: float, eps: float):
    grish = GrishaginFunction(i)
    y_opt = grish.GetOptimumPoint()
    z_opt = grish.Calculate(y_opt)
    problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
    stop = StopCondition(eps, 100000)
    param = Parameters(r)
    solver = SequentialSolver(problem, stop, param)
    solver.solve()
    sol = solver.solution
    print(f"Grishagin {i}")
    print(f"Solution point: {y_opt},")
    print(f"Solution value: {z_opt},")
    print(f"Calculated point: {sol.optimumPoint},")
    print(f"Calculated value: {sol.optimumValue},")
    print(f"Iteration count: {sol.niter}")


if __name__ == "__main__":
    seq_alg_grishagin(31, 4, 0.01)
