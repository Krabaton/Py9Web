from multiprocessing import Process, RLock, Value, Array
from random import randint
from time import sleep
from ctypes import c_int

POOL_SIZE = 5
lock = RLock()
counter = Value(c_int, 0)
array = Array('i', range(POOL_SIZE))


def example_work(counter: Value, lock: RLock, arr: Array, index: int):
    while True:
        with lock:
            counter.value = counter.value + 1
            arr[index] = counter.value
            sleep(randint(1, 2))
            with open('result.txt', 'a') as fa:
                fa.write(f'{counter.value}\n')


if __name__ == '__main__':
    print('Start program')
    for i in range(POOL_SIZE):
        pr = Process(target=example_work, args=(counter, lock, array, i), daemon=True)  # daemon=True
        pr.start()

    sleep(3)

    print(array[:])
    print('End program')
