from threading import Event, Thread
from time import sleep
import logging


def worker_timeout(event: Event, time: float):
    while not event.is_set():
        logging.debug('Чекаємо поки флаг event не буде встановлений')
        e_wait = event.wait(time)
        if e_wait:
            logging.debug('Починаємо виконувати якусь роботу')
        else:
            logging.debug('Флаг ще не встановили чекаємо')


def worker(event: Event):
    logging.debug(f'waiting...')
    event.wait()
    # some work
    logging.debug(f'finished')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    e = Event()

    th = Thread(target=worker, args=(e, ))
    th.start()
    th_timeout = Thread(target=worker_timeout, args=(e, 1))
    th_timeout.start()

    sleep(3)
    e.set()

    logging.debug('End program')
