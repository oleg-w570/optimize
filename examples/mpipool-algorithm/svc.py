import os
import sys

sys.path.append(os.getcwd())
from modules.solve import solve
from problems.svc.svc import SVC_2D


if __name__ == "__main__":
    problem = SVC_2D()
    print(problem)
    print(solve(problem, r=4, eps=0.01, alg="mpipool", num_proc=4))
