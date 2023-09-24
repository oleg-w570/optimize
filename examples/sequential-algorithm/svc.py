from sklearn.datasets import load_breast_cancer
from sklearn.utils import shuffle

from modules.sequential_solver import SequentialSolver
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from problems.svc import SVC_2D


def load_breast_cancer_data():
    dataset = load_breast_cancer()
    x_raw, y_raw = dataset['data'], dataset['target']
    inputs, outputs = shuffle(x_raw, y_raw ^ 1, random_state=42)
    return inputs, outputs


def seq_alg_svc(r: float, eps: float):
    x, y = load_breast_cancer_data()
    regularization_value_bound = {'low': 1, 'up': 6}
    kernel_coefficient_bound = {'low': -7, 'up': -3}
    svc = SVC_2D(x, y, regularization_value_bound, kernel_coefficient_bound)
    # y_opt = gkls.GetOptimumPoint()
    # z_opt = gkls.GetOptimumValue()
    problem = Problem(svc.calculate, svc.lower_bound, svc.upper_bound, 2)
    stop = StopCondition(eps, 10000)
    param = Parameters(r)
    solver = SequentialSolver(problem, stop, param)
    solver.solve()
    sol = solver.solution
    print("SVC 2D")
    # print(f"Solution point: {y_opt},")
    # print(f"Solution value: {z_opt},")
    print(f"Calculated point: {sol.optimum.y},")
    print(f"Calculated value: {sol.optimum.z},")
    print(f"Iteration count: {sol.niter}")
    print(f'Solution time: {sol.time}')


if __name__ == "__main__":
    seq_alg_svc(3, 0.001)
