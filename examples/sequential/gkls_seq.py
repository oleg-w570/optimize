from modules.solve import solve
from problems.gkls.gkls import GKLS


if __name__ == "__main__":
    problem = GKLS(23)
    print(problem)
    print(solve(problem, r=3.5, eps=0.01, alg="seq"))
