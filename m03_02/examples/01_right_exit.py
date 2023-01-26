from multiprocessing import Process, Manager
from time import sleep
import sys


def worker(name, delay, value):
    print(f'{name} started!')
    sleep(delay)
    value[name] = 42
    print(f'{name} finished!')
    sys.exit(0)  # Если не ноль, то это код ошибки


if __name__ == '__main__':
    with Manager() as manager:
        val = manager.dict()
        pr1 = Process(target=worker, args=('first', 2, val))
        pr2 = Process(target=worker, args=('second', 2, val))

        pr1.start()
        pr2.start()
        print('All started!')
        print(pr1.exitcode, pr2.exitcode)
        pr1.join()
        pr2.join()
        print(pr1.exitcode, pr2.exitcode)
        print(val)
