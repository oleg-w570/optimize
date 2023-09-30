import os
import sys
sys.path.append(os.getcwd())
from modules.solve import solve
from problems.gkls.gkls import GKLS


if __name__ == "__main__":
    problem = GKLS(92)
    print(problem)
    print(
        solve(problem,
              r=4, eps=0.01,
              alg='mpi')
    )
