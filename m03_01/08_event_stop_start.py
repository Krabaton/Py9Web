from threading import Event, Thread
from time import sleep
import logging


def worker(event: Event, event_for_exit: Event):
    while True:
        sleep(1)
        if event_for_exit.is_set():
            break

        if event.is_set():
            continue
        else:
            logging.debug(f'Run iteration')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    e = Event()  # stop - set, start - clear
    e_exit = Event()

    th = Thread(target=worker, args=(e, e_exit))
    th.start()
    logging.debug('Start!')
    sleep(3)
    e.set()
    logging.debug('Stop!')
    sleep(2)
    e.clear()
    logging.debug('Start!')
    sleep(3)
    e_exit.set()
    logging.debug('End program')
