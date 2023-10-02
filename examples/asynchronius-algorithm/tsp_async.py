import xml.etree.ElementTree as ET

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


if __name__ == "__main__":
    tsp_matrix = load_tsp_matrix("../../a280.xml")
    num_iteration = 200
    mutation_probability_bound = {"low": 0.0, "up": 1.0}
    population_size_bound = {"low": 10.0, "up": 100.0}
    problem = TSP_2D(
        tsp_matrix, num_iteration, mutation_probability_bound, population_size_bound
    )
    print(problem)
    print(solve(problem, r=4, eps=0.01, alg="async"))
