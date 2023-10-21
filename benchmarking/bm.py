from statistics import mean

import numpy as np
import xml.etree.ElementTree as ET
import pandas as pd

from modules.solve import solve
from problems.gkls.gkls import GKLS
from problems.svc.svc import SVC_2D
from problems.tsp.tsp import TSP_2D

r = 4.05
algorithms = ['seq', 'pool', 'async']
number_of_processes = [2, 4]
num_launches = 10


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


def calculate_data(launches):
    data = {}
    name = 'GKLS (eps)'
    data[(name, 'time')] = []
    data[(name, 'value')] = []
    for alg, n in launches:
        all_time = []
        all_div = []
        for i in range(1, 101):
            problem = GKLS(i)
            sol = solve(problem, r=r, eps=0.01, alg=alg, num_proc=n)
            all_time.append(sol.time)
            all_div.append(1 + sol.optimum.z)
        data[(name, 'time')].append(mean(all_time))
        data[(name, 'value')].append(mean(all_div))

    name = 'GKLS (iter)'
    data[(name, 'time')] = []
    data[(name, 'value')] = []
    for alg, n in launches:
        all_time = []
        all_div = []
        for i in range(1, 101):
            problem = GKLS(i)
            sol = solve(problem, r=r, eps=0.00000001, max_iter=1000, alg=alg, num_proc=n)
            all_time.append(sol.time)
            all_div.append(1 + sol.optimum.z)
        data[(name, 'time')].append(mean(all_time))
        data[(name, 'value')].append(mean(all_div))

    name = 'SVC_2D'
    data[(name, 'time')] = []
    data[(name, 'value')] = []
    problem = SVC_2D()
    for alg, n in launches:
        all_time = []
        all_value = []
        for _ in range(num_launches):
            sol = solve(problem, r=r, eps=0.0000001, max_iter=1000, alg=alg, num_proc=n)
            all_time.append(sol.time)
            all_value.append(sol.optimum.z)
        data[(name, 'time')].append(mean(all_time))
        data[(name, 'value')].append(mean(all_value))

    name = 'TSP_2D'
    data[(name, 'time')] = []
    data[(name, 'value')] = []
    tsp_matrix = load_tsp_matrix("../a280.xml")
    num_iteration = 200
    mutation_probability_bound = {"low": 0.0, "up": 1.0}
    population_size_bound = {"low": 10.0, "up": 100.0}
    problem = TSP_2D(tsp_matrix, num_iteration, mutation_probability_bound, population_size_bound)
    for alg, n in launches:
        all_time = []
        all_value = []
        for _ in range(num_launches):
            sol = solve(problem, r=r, eps=0.0000001, max_iter=200, alg=alg, num_proc=n)
            all_time.append(sol.time)
            all_value.append(sol.optimum.z)
        data[(name, 'time')].append(mean(all_time))
        data[(name, 'value')].append(mean(all_value))

    return data


def format_data(data, launches):
    df = pd.DataFrame(data)
    df = df.rename_axis('Схема решения')
    df = df.rename(columns={
        'GKLS (eps)': 'GKLS (с задержкой в функции 0.01 сек.)\nПараметр метода r=4\nОстановка по точности eps=0.01',
        'GKLS (iter)': "GKLS (с задержкой в функции 0.01 сек.)\nПараметр метода r=4\nОстановка по числу испытаний 1000",
        'TSP_2D': "TSP_2D\nПараметр метода r=4\nОстановка по числу испытаний 200",
        'SVC_2D': "SVC_2D\nПараметр метода r=4\nОстановка по числу испытаний 1000",
        'time': 'Время вычисления (сек.)',
        'value': 'Результат'
    })
    index_names = {}
    for i, launch in enumerate(launches):
        alg, n = launch
        match alg:
            case 'seq': name = 'Последовательная'
            case 'pool': name = 'Параллельная синхронная'
            case 'async': name = 'Параллельная асинхронная'
            case _: name = ''
        index_names[i] = f'{name}\nЧисло процессов: {n}'
    df = df.rename(index=index_names)
    return df


def create_launches():
    launches = []
    if 'seq' in algorithms:
        launches.append(('seq', 1))
        algorithms.remove('seq')
    for n in number_of_processes:
        for alg in algorithms:
            launches.append((alg, n))
    return launches


def main():
    launches = create_launches()
    data = calculate_data(launches)
    data = format_data(data, launches)
    data.to_excel('results/benchmark.xlsx', float_format='%.3f')


if __name__ == '__main__':
    main()
