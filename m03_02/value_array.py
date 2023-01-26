from multiprocessing import Process, current_process, RLock, Value, Array
from random import randint
from time import sleep
from ctypes import c_int, c_double, Structure
from sys import exit


class Point(Structure):
    _fields_ = [('x', c_double), ('y', c_double)]


def worker(val: Value, string: Array, arr: Array):
    print(f"Start process: {current_process().name}")
    with val.get_lock():
        val.value += 1
        print(f"Process: {current_process().name}: {val.value}")
    with string.get_lock():
        string.value = string.value.upper()
    with arr.get_lock():
        for el in arr:
            el.x += val.value
            el.y += val.value
    exit(0)


if __name__ == '__main__':
    print('Start program')
    lock = RLock()
    value = Value(c_double, 1.5, lock=lock)
    string = Array('c', b'The best group 9', lock=lock)
    arr = Array(Point, [(0, 0), (2, 0), (2, 2)], lock=lock)

    process = []

    for i in range(3):
        pr = Process(target=worker, args=(value, string, arr))  # daemon=True
        pr.start()
        process.append(pr)

    [pr.join() for pr in process]
    [print(pr.exitcode) for pr in process]
    print(value.value)
    print(string.value)
    [print(el.x, el.y) for el in arr]
    print('End program')
