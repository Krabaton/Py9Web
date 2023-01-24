import logging
from random import randint
from threading import Barrier, Thread, current_thread
from time import sleep, ctime


def worker(barrier: Barrier):
    name = current_thread().name
    logging.debug(f"Start thread {name}: {ctime()}")
    sleep(randint(1, 3))
    num = barrier.wait()
    logging.debug(f"{num}")
    logging.debug(f'Бар\'єр подоланий {name}: {ctime()}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    br = Barrier(3)

    for i in range(12):
        th = Thread(target=worker, args=(br, ))
        th.start()

