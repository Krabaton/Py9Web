from threading import Event, Thread
from time import sleep
import logging


def master(event: Event):
    sleep(1)  # Some work
    logging.debug('Set event...')
    event.set()


def worker(event: Event):
    logging.debug(f'waiting...')
    event.wait()
    # some work
    logging.debug(f'finished')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    e = Event()

    m = Thread(target=master, args=(e, ))
    w2 = Thread(target=worker, args=(e, ))
    w1 = Thread(target=worker, args=(e, ))

    w1.start()
    w2.start()
    m.start()
