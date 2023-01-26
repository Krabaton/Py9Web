from multiprocessing import Process, Semaphore, current_process, Manager
from random import randint
from time import sleep


def worker(semaphore: Semaphore, r: dict):
    print('Wait')
    with semaphore:
        name = current_process().name
        print(f'Work {name}')
        delay = randint(1, 2)
        r[name] = delay
        sleep(0.2)  # Имитируем какую-то работу


if __name__ == '__main__':
    semaphore = Semaphore(3)
    with Manager() as m:
        result = m.dict()  # Plain
        prs = []
        for num in range(10):
            pr = Process(name=f'Process-{num}', target=worker, args=(semaphore, result))
            pr.start()
            prs.append(pr)

        for pr in prs:
            pr.join()

        print(result)

    print('End program')