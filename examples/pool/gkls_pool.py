from modules.solve import solve
from problems.gkls.gkls import GKLS


if __name__ == "__main__":
    problem = GKLS(1)
    print(problem)
    print(solve(problem, r=4.05, eps=0.01, alg="pool", num_proc=4))
