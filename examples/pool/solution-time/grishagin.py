from statistics import mean

from modules.solve import solve
from problems.grishagin.grishagin import Grishagin

if __name__ == "__main__":
    r = 4
    eps = 0.01
    n = 4
    solution_time = []
    for i in range(1, 101):
        problem = Grishagin(i)
        print(problem)
        sol = solve(problem,
                    r=r, eps=eps,
                    alg='pool', num_proc=n)
        print(sol)
        solution_time.append(sol.time)
        print("--------------------------------------")
    max_solution_time = max(solution_time)
    avg_solution_time = mean(solution_time)
    print("Grishagin functions")
    print("Parallel algorithm")
    print(f"r = {r}, eps = {eps}")
    print(f"Max solution time: {max_solution_time} sec.")
    print(f"Average solution time: {avg_solution_time} sec.")
