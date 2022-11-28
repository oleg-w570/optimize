from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
from jmetal.algorithm.singleobjective.evolution_strategy import EvolutionStrategy
from jmetal.operator import PolynomialMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from test_functions import generateHH, generateSH
import numpy as np
rng = np.random.RandomState()


class HH(FloatProblem):
    def __init__(self, number_of_variables: int = 1):
        super(HH, self).__init__()
        self.funcHH = generateHH()

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
    def __init__(self, number_of_variables: int = 1):
        super(SH, self).__init__()
        self.funcSH = generateSH()

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


problem = HH()
algorithm = EvolutionStrategy(problem=problem,  mu=10, lambda_=10, elitist=True, mutation=PolynomialMutation(probability=1.0), termination_criterion=StoppingByEvaluations(max_evaluations=25000))
algorithm.run()
result = algorithm.get_result()

print(result)



