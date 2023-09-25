import os
import sys
sys.path.append(os.getcwd())

from problems.gkls.gkls import GKLS
from modules.solve import solve


if __name__ == "__main__":
    problem = GKLS(10)
    print(problem)
    print(
        solve(problem,
              r=4, eps=0.01,
              alg='mpi')
    )
