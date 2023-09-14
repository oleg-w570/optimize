from multiprocessing import Queue

q = Queue()
for i in range(10):
    q.put(i**2)

for n in iter(q.get, 64):
    print(n)
