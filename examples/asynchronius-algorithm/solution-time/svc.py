from statistics import mean
from modules.solve import solve
from problems.svc.svc import SVC_2D

if __name__ == "__main__":
    r = 4
    eps = 0.01
    n = 4
    solution_time = []
    for _ in range(100):
        problem = SVC_2D()
        print(problem)
        sol = solve(problem,
                    r=r, eps=eps,
                    alg='async', num_proc=n)
        print(sol)
        solution_time.append(sol.time)
        print("--------------------------------------")
    max_solution_time = max(solution_time)
    avg_solution_time = mean(solution_time)
    print("SVC_2D functions")
    print("Parallel algorithm (async)")
    print(f"r = {r}, eps = {eps}, n={n}")
    print(f"Max solving time: {max_solution_time} sec")
    print(f"Average solving time: {avg_solution_time} sec.")

