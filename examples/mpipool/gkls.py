from modules.solve import solve
from problems.gkls.gkls import GKLS


if __name__ == "__main__":
    problem = GKLS(10)
    print(problem)
    print(solve(problem, r=4, eps=0.01, alg="mpipool", num_proc=4))
