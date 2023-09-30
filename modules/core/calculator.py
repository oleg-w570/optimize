from modules.utility.problem import Problem


class Calculator:
    problem: Problem | None = None

    @staticmethod
    def worker_init(problem: Problem):
        Calculator.problem = problem

    @staticmethod
    def work(y: list[float]) -> float:
        z = Calculator.problem.calculate(y)
        return z


