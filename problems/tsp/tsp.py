from sko.GA import GA_TSP

from modules.utility.problem import Problem


class TSP_2D(Problem):
    def __init__(
        self,
        cost_matrix,
        num_iteration: int,
        mutation_probability_bound: dict[str, float],
        population_size_bound: dict[str, float],
    ):
        super().__init__()
        self.name = "TSP_2D"
        self.dim = 2
        self.lower_bound = [
            mutation_probability_bound["low"],
            population_size_bound["low"],
        ]
        self.upper_bound = [
            mutation_probability_bound["up"],
            population_size_bound["up"] / 2,
        ]
        self.cost_matrix = cost_matrix
        self.n_dim = cost_matrix.shape[0]
        self.num_iteration = num_iteration

    def total_distance(self, routine):
        num_points, = routine.shape
        return sum(
            [
                self.cost_matrix[routine[i % num_points], routine[(i + 1) % num_points]]
                for i in range(num_points)
            ]
        )

    def calculate(self, point: list[float]) -> float:
        mutation_prob, num_population = point[0], int(point[1])
        num_population -= num_population % 2
        ga_tsp = GA_TSP(func=self.total_distance,
                        n_dim=self.n_dim, size_pop=num_population,
                        max_iter=int(self.num_iteration), prob_mut=mutation_prob)
        best_points, best_distance = ga_tsp.run()
        return best_distance[0]

