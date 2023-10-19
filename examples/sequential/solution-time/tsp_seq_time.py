import xml.etree.ElementTree as ET
from statistics import mean

import numpy as np

from modules.solve import solve
from problems.tsp.tsp import TSP_2D


def load_tsp_matrix(file_name):
    root = ET.parse(file_name).getroot()
    columns = root.findall("graph/vertex")
    num_cols = len(columns)
    trans_matrix = np.zeros((num_cols, num_cols))
    for i, v in enumerate(columns):
        for e in v:
            j = int(e.text)
            trans_matrix[i, j] = float(e.get("cost"))
    return trans_matrix


def create_problem():
    tsp_matrix = load_tsp_matrix("../../../a280.xml")
    num_iteration = 200
    mutation_probability_bound = {"low": 0.0, "up": 1.0}
    population_size_bound = {"low": 10.0, "up": 100.0}
    problem_tsp = TSP_2D(
        tsp_matrix, num_iteration, mutation_probability_bound, population_size_bound
    )
    return problem_tsp


if __name__ == "__main__":
    problem = create_problem()
    r = 4
    eps = 0.00001
    max_iter = 200
    num_launches = 10
    time = []
    res = []
    for i in range(num_launches):
        print(i)
        sol = solve(problem,
                    r=r, eps=eps, max_iter=max_iter,
                    alg='seq')
        time.append(sol.time)
        res.append(sol.optimum.z)
        print(f'Time: {sol.time}')
        print(f'Value: {sol.optimum.z}')
        print('-----------------------')
    print(f"{num_launches} launches of TSP_2D")
    print("Sequential algorithm")
    print(f"r={r}, max_iter={max_iter}")
    print(f"Average solution time: {mean(time)}")
    print(f"Average value: {mean(res)}")
