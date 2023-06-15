from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
from jmetal.algorithm.singleobjective.evolution_strategy import EvolutionStrategy
from jmetal.operator import PolynomialMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from problems.hill_function import HillFunction
from problems.shekel_function import ShekelFunction
import numpy as np


class HH(FloatProblem):
    def __init__(self, funcHH: callable, number_of_variables: int = 1):
        super(HH, self).__init__()
        self.funcHH = funcHH

        self.number_of_objectives = 1
        self.number_of_variables = number_of_variables
        self.number_of_constraints = 0

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ["f(x)"]

        self.lower_bound = [0]
        self.upper_bound = [1]

        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        x = solution.variables[0]
        res = self.funcHH(x)
        solution.objectives[0] = res

        return solution

    def get_name(self) -> str:
        return "HH"


class SH(FloatProblem):
    def __init__(self, funcSH: callable, number_of_variables: int = 1):
        super(SH, self).__init__()
        self.funcSH = funcSH

        self.number_of_objectives = 1
        self.number_of_variables = number_of_variables
        self.number_of_constraints = 0

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ["f(x)"]

        self.lower_bound = [0]
        self.upper_bound = [10]

        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        x = solution.variables[0]
        res = self.funcSH(x)
        solution.objectives[0] = res

        return solution

    def get_name(self) -> str:
        return "SH"


# right_border = 1
# eps = 1e-3
# max_niter = 351
# step = 10
# N = 100
def jmetal_op(test_func_class: str, max_niter, eps, N, step):
    percent_right_solved = []
    right_border = 1 if test_func_class == 'HL' else 10
    for niter in range(0, max_niter, step):
        solved = 0
        for i in range(0, N):
            f = HillFunction() if test_func_class == 'HL' else ShekelFunction()
            minimum = min(map(f, np.arange(0, right_border, eps)))
            problem = HH(f) if test_func_class == 'HL' else SH(f)
            algorithm = EvolutionStrategy(problem, mu=10, lambda_=10, elitist=True,
                                          mutation=PolynomialMutation(probability=1.0),
                                          termination_criterion=StoppingByEvaluations(max_evaluations=niter))
            algorithm.run()
            result = algorithm.get_result().objectives[0]
            if result < minimum + 1e-2:
                solved += 1
            else:
                print("Неверное решение! Правильно:", minimum, "имеем:", result)
        percent_right_solved.append(solved/N*100)
    return percent_right_solved

# x1 = range(0, max_niter, step)
# y1 = percent_right_solved
# plt.style.use('seaborn-v0_8')
# plt.title('Операционная характеристика\nЭверистическего метода jmetal\nФункции из класса HH')
# plt.xlabel('Число итераций')
# plt.ylabel('% решённых задач')
# plt.plot(x1, y1, linewidth=1)
# plt.legend()
# plt.show()
