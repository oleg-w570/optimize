from matplotlib import pyplot as plt
from mpi4py import MPI
from modules.core.mpisolver import MpiSolver
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from problems.grishagin_function import GrishaginFunction


def TestMpi():
    # k = random.randint(1, 100)
    k = 43
    grish = GrishaginFunction(k)
    y_opt = grish.GetOptimumPoint()
    z_opt = grish.Calculate(y_opt)

    problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
    stop = StopCondition(0.01, 1000)
    param = Parameters(2.5, 4)
    solver = MpiSolver(problem, stop, param)
    solver.solve()

    if MPI.COMM_WORLD.rank == 0:
        sol = solver.solution
        print(f"Grishagin {k}")
        print(f"Solution point: {y_opt},")
        print(f"Solution value: {z_opt},")
        print(f"My point: {sol.optimum.y},")
        print(f"My value: {sol.optimum.z},")
        print(f"Accuracy: {sol.accuracy}")
        print(f"Iteration count: {sol.iterationCount}")

def MPIOp():
    global allIters, z_opt, y_opt
    r = 4
    eps = 0.01
    rank = MPI.COMM_WORLD.rank
    numberOfProcess = [1, 2, 4]
    plt.style.use('seaborn-v0_8')
    for n in numberOfProcess:
        if rank == 0:
            allIters = []
        for i in range(1, 101):
            # if i == 43 or i == 76:
            #     continue
            grish = GrishaginFunction(i)
            if rank == 0:
                y_opt = grish.GetOptimumPoint()
                z_opt = grish.Calculate(y_opt)
            problem = Problem(grish.Calculate, [0, 0], [1, 1], 2)
            stop = StopCondition(eps, 10000)
            param = Parameters(r, n)
            solver = MpiSolver(problem, stop, param)
            solver.solve()
            if rank == 0:
                sol = solver.solution
                if sol.optimum.z < z_opt + 9e-2:
                    allIters.append(sol.iterationCount)
                print(f"Grishagin {i}")
                print(f"Solution point: {y_opt},")
                print(f"Solution value: {z_opt},")
                print(f"My point: {sol.optimum.y},")
                print(f"My value: {sol.optimum.z},")
                print(f"Accuracy: {sol.accuracy}")
                print(f"Iteration count: {sol.iterationCount}")
                print(f"Number of processes: {n}")
                print(f"-------------------------------------")
        if rank == 0:
            acc = 0
            percent = []
            for i in range(0, max(allIters)+1):
                acc += allIters.count(i)
                percent.append(acc)
            plt.plot(range(0, max(allIters)+1), percent, linewidth=1, label=f"{n} pool_size")
    if rank == 0:
        plt.title(f'Операционная характеристика\nПараллельная версия АГП на MPI\nФункции Гришагина\n'
                  f'r = {r}, eps = {eps}, mpi_size = {MPI.COMM_WORLD.size}')
        plt.xlabel('Число проведённых испытаний')
        plt.ylabel('% решённых задач')
        plt.legend()
        plt.show()
