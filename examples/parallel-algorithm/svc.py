from sklearn.datasets import load_breast_cancer
from sklearn.utils import shuffle

from modules.parallel_solver import ParallelSolver
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from problems.svc import SVC_2D


def parallel_alg_svc(n: int, r: float, eps: float):
    x, y = load_breast_cancer_data()
    regularization_value_bound = {'low': 1, 'up': 6}
    kernel_coefficient_bound = {'low': -7, 'up': -3}
    svc = SVC_2D(x, y, regularization_value_bound, kernel_coefficient_bound)
    # y_opt = gkls.GetOptimumPoint()
    # z_opt = gkls.GetOptimumValue()
    problem = Problem(svc.calculate, svc.lower_bound, svc.upper_bound, 2)
    stop = StopCondition(eps, 10000)
    param = Parameters(r, n)
    solver = ParallelSolver(problem, stop, param)
    solver.solve()
    sol = solver.solution
    print("SVC 2D")
    # print(f"Solution point: {y_opt},")
    # print(f"Solution value: {z_opt},")
    print(f"Calculated point: {sol.optimum.y},")
    print(f"Calculated value: {sol.optimum.z},")
    print(f"Iteration count: {sol.niter}")


def load_breast_cancer_data():
    dataset = load_breast_cancer()
    x_raw, y_raw = dataset['data'], dataset['target']
    inputs, outputs = shuffle(x_raw, y_raw ^ 1, random_state=42)
    return inputs, outputs


if __name__ == "__main__":
    parallel_alg_svc(4, 4, 0.01)
