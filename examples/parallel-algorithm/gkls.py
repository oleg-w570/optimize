from modules.parallel_solver import ParallelSolver
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from problems.gkls_function import GKLSFunction, GKLSClass


def parallel_alg_gkls(i: int, n: int, r: float, eps: float):
    gkls = GKLSFunction()
    gkls.SetDimension(3)
    gkls.SetFunctionClass(GKLSClass.Simple, 3)
    gkls.SetFunctionNumber(i)
    y_opt = gkls.GetOptimumPoint()
    z_opt = gkls.GetOptimumValue()
    problem = Problem(gkls.Calculate, [-1, -1, -1], [1, 1, 1], 3)
    stop = StopCondition(eps, 10000)
    param = Parameters(r, n)
    solver = ParallelSolver(problem, stop, param)
    solver.solve()
    sol = solver.solution
    print(f"GKLS {i}")
    print(f"Solution point: {y_opt},")
    print(f"Solution value: {z_opt},")
    print(f"Calculated point: {sol.optimum.y},")
    print(f"Calculated value: {sol.optimum.z},")
    print(f"Iteration count: {sol.niter}")


if __name__ == "__main__":
    parallel_alg_gkls(66, 4, 4, 0.01)
