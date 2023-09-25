from modules.mpi_pool_solver import MPIPoolSolver
from modules.mpi_solver import MPISolver
from modules.parallel_solver import ParallelSolver
from modules.sequential_solver import SequentialSolver
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.solution import Solution
from modules.utility.stopcondition import StopCondition


def solve(problem: Problem, *,
          eps: float = 0.01, max_iter: int = 100000,
          alg: str = 'seq', num_proc: int = 4,
          r: float = 4
          ) -> Solution:
    stop = StopCondition(eps, max_iter)
    param = Parameters(r, num_proc)
    match alg:
        case 'seq':
            solver = SequentialSolver(problem, stop, param)
        case 'parallel':
            solver = ParallelSolver(problem, stop, param)
        case 'mpi':
            solver = MPISolver(problem, stop, param)
        case 'mpipool':
            solver = MPIPoolSolver(problem, stop, param)
        case _:
            print('Wrong algorithm')
            return Solution()
    solver.solve()
    return solver.solution



