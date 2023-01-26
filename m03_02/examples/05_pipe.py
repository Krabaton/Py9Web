from multiprocessing import Process, Pipe
from time import sleep
import sys


def worker(conn: Pipe, name):
    print(f'{name} started!')
    val = conn.recv()
    print(f'{name} {val ** 2}')
    sys.exit(0)  # Если не ноль, то это код ошибки


if __name__ == '__main__':
    rcv1, snd1 = Pipe(duplex=False)
    rcv2, snd2 = Pipe(duplex=False)

    pr1 = Process(target=worker, args=(rcv1, 'first'))
    pr2 = Process(target=worker, args=(rcv2, 'second'))

    pr1.start()
    pr2.start()

    snd1.send(10)
    sleep(2)
    snd2.send(5)
