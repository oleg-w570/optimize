import testing.mpipool_test as mpipool
import testing.parallel_test as parallel
import testing.ndim_test as seq
import testing.mpi_test as mpi
from modules.core.evolvent import Evolvent
from c_implementation.myevolvent import Evolvent as MyEvo
from time import perf_counter

if __name__ == '__main__':
    # evo = Evolvent([0, 0], [1, 1], 2)
    # my_evo = MyEvo([0, 0], [1, 1], 2)
    # x = 0.991
    # start = perf_counter()
    # y = evo.GetImage(x)
    # print(f"time: {perf_counter()-start}")
    # print(f"{x} -> {y}\n\n")
    #
    # start = perf_counter()
    # y = my_evo.GetImage(x)
    # print(f"time: {perf_counter()-start}")
    # print(f"my value: {x} -> {y}")
    #
    #
    # mpi.grish_time()
    # mpi.gkls(24)
    # mpi.grish_op()
    # parallel.grish_time()
    # parallel.grish_op()
    # parallel.gkls_op()
    # parallel.gksl(35)
    # mpipool.gkls_op()
    # mpipool.grish_time()
    # seq.gkls_op()
    # seq.gksl(18)
    # seq.grish_op()
    # seq.grish_time()
    # seq.gkls_time()
    mpi.gkls_time()
