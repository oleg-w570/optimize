from statistics import mean

from mpi4py import MPI

from modules.solve import solve
from problems.gkls.gkls import GKLS


if __name__ == "__main__":
    r = 4
    eps = 0.01
    rank = MPI.COMM_WORLD.Get_rank()
    solution_time = []
    for i in range(1, 101):
        problem = GKLS(i)
        print(problem)
        sol = solve(problem,
                    r=r, eps=eps,
                    alg='mpi')
        print(sol)
        solution_time.append(sol.time)
        print("--------------------------------------")
    max_solution_time = max(solution_time)
    avg_solution_time = mean(solution_time)
    print("GKLS functions")
    print("Parallel algorithm (mpi)")
    print(f"r = {r}, eps = {eps}")
    print(f"Max solving time: {max_solution_time} sec")
    print(f"Average solving time: {avg_solution_time} sec.")

