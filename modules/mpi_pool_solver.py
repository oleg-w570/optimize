from time import perf_counter
from modules.utility.interval import Interval
from modules.utility.point import Point
from modules.core.solver import Solver
from itertools import chain
from mpi4py import MPI
from pathos.pools import ProcessPool


class MPIPoolSolver(Solver):
    def get_intrvls_with_max_r(self) -> list[list[Interval]]:
        intrvls: list[Interval] = []
        for _ in range(min(MPI.COMM_WORLD.size * self.num_proc, self.trial_data.size())):
            intrvls.append(self.trial_data.get_intrvl_with_max_r())
        step = len(intrvls) // MPI.COMM_WORLD.size
        return [intrvls[i:i + step] for i in range(0, len(intrvls), step)]
    
    def solve(self):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()

        self.first_iteration()
        self.sequential_iterations_for_begin()

        mindelta: float = float('inf')
        niter: int = 0

        with ProcessPool(self.num_proc) as pool:
            start_time = perf_counter()
            while mindelta > self.stop.eps and niter < self.stop.maxiter:
                if rank == 0:
                    all_old_intrvls = self.get_intrvls_with_max_r()
                else:
                    all_old_intrvls = None
                loc_old_intrvls: list[Interval] = comm.scatter(all_old_intrvls, 0)

                loc_mindelta: float = min(loc_old_intrvls, key=(lambda x: x.delta)).delta
                mindelta = comm.allreduce(loc_mindelta, MPI.MIN)

                loc_points: list[Point] = pool.map(self.method.next_point, loc_old_intrvls)
                loc_minpoint: Point = min(loc_points)
                minpoint: Point = comm.allreduce(loc_minpoint, MPI.MIN)
                self.recalc |= self.method.update_optimum(minpoint)

                loc_new_intrvls = pool.map(self.method.split_interval, loc_old_intrvls, loc_points)
                loc_new_intrvls = list(chain.from_iterable(loc_new_intrvls))
                all_new_intrvls = comm.gather(loc_new_intrvls, 0)

                loc_new_m: list[float] = pool.map(self.method.holder_const, loc_new_intrvls)
                loc_max_m: float = max(loc_new_m)
                max_m: float = comm.allreduce(loc_max_m, MPI.MAX)
                self.recalc |= self.method.update_holder_const(max_m)

                loc_new_r: list[float] = pool.map(self.method.characteristic, loc_new_intrvls)
                all_new_r: list[list[float]] = comm.gather(loc_new_r, 0)
                if rank == 0:
                    self.recalculate()
                    all_new_intrvls = list(chain.from_iterable(all_new_intrvls))
                    all_new_r = list(chain.from_iterable(all_new_r))

                    for trial in zip(all_new_r, all_new_intrvls):
                        self.trial_data.insert(*trial)
                niter += 1
                self._solution.time = perf_counter() - start_time
            self._solution.accuracy = mindelta
            self._solution.niter = niter

    def sequential_iterations_for_begin(self):
        for _ in range(MPI.COMM_WORLD.size-1):
            old_intrvl: Interval = self.trial_data.get_intrvl_with_max_r()
            point: Point = self.method.next_point(old_intrvl)
            new_intrvl = self.method.split_interval(old_intrvl, point)
            new_m = map(self.method.holder_const, new_intrvl)
            self.recalc |= self.method.update_holder_const(max(new_m))
            self.recalc |= self.method.update_optimum(point)
            self.recalculate()
            new_r = map(self.method.characteristic, new_intrvl)
            for trial in zip(new_r, new_intrvl):
                self.trial_data.insert(*trial)
