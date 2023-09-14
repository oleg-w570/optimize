from multiprocessing import Process, Queue, current_process, freeze_support
from queue import PriorityQueue
import random
from time import sleep


def worker(input: Queue, output: Queue):
    for intrvl in iter(input.get, 'STOP'):
        point = (intrvl[1][0] + intrvl[1][1]) * 0.5
        left_intrvl = [intrvl[1][0], point]
        right_intrvl = [point, intrvl[1][1]]
        sleep(random.randint(0, 1))
        print(f'\t{current_process().name} calculated intervals {left_intrvl} and {right_intrvl}')
        output.put((random.randint(0, 100), left_intrvl))
        output.put((random.randint(0, 100), right_intrvl))


def test():
    NUM_PROC = 4

    intrvls = PriorityQueue()
    task_queue = Queue()
    done_queue = Queue()

    task_queue.put((0, [0, 10]))

    for _ in range(NUM_PROC):
        Process(target=worker, args=(task_queue, done_queue)).start()

    while True:
        new_intrvl = done_queue.get()
        if new_intrvl[1][1] - new_intrvl[1][0] < 0.5:
            break
        intrvls.put(new_intrvl)
        task_queue.put(intrvls.get())

    for _ in range(NUM_PROC):
        task_queue.put('STOP')


if __name__ == "__main__":
    freeze_support()
    test()
