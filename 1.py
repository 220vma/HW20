from datetime import datetime
from queue import Queue
from time import sleep
from threading import Thread

TAMOUNT = 2

def is_prime(number):
    if number <= 2:
        return True
    if number % 2 == 0:
        return False
    for i in range(3, int(number**0.5 + 1)):
        if number % i == 0:
            return False
    return True

def queue_maker(q: Queue, id):
    print(f'start {id} queue_maker')
    while True:
        number = q.get()
        if number is None:
            break
        if is_prime(number):
            print(id, number)
    print(f'stop {id} queue_maker')

def generator(q: Queue):
    print('generator start')
    max_size = 50
    for i in range(1, 1_000_000):
        q.put(i)
    for i in range(TAMOUNT):
        q.put(None)
    print('generator stop')

start = datetime.now()
q = Queue()
gthread = Thread(target=generator, args=(q,))
makers = []
for i in range(TAMOUNT):
    m = Thread(target=queue_maker, args=(q, i+1))
    m.start()
    makers.append(m)

gthread.start()
gthread.join()

for i in range(TAMOUNT):
    makers[i].join()
duration_threads = datetime.now() - start

start = datetime.now()
for i in range(1, 1_000_000):
    if is_prime(i):
        print(i)
duration = datetime.now() - start
print(f'Время выполнения (без потоков): {duration}')
print(f'Время выполнения (3 потока без sleep): {duration_threads}')