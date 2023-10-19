from modules.solve import solve
from problems.grishagin.grishagin import Grishagin

if __name__ == "__main__":
    problem = Grishagin(10)
    print(problem)
    print(solve(problem, r=4, eps=0.01, alg="seq"))
