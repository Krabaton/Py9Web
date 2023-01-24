from threading import Event, Thread
from time import sleep
import logging


def worker(event: Event):
    while True:
        sleep(1)
        logging.debug(f'Run iteration')

        if event.is_set():
            break


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    e = Event()

    th = Thread(target=worker, args=(e, ))
    th.start()

    sleep(3)
    e.set()

    logging.debug('End program')
