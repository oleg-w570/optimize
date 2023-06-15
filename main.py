import testing.mpipool_test as mpipool
import testing.parallel_test as parallel
import testing.ndim_test as seq
import testing.mpi_test as mpi


if __name__ == '__main__':
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
    seq.gksl(35)
    # seq.grish_op()
    # seq.grish_time()
