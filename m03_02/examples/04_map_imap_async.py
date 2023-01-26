from multiprocessing import Pool
import time


def worker(val):
    return val ** 2


if __name__ == '__main__':

    with Pool(2) as pool:
        result = pool.apply_async(worker, (10, ))
        print(result.get())

        r = pool.map(worker, range(10))
        print(r)

        iterator = pool.imap(worker, range(10))
        print(next(iterator))
        print(next(iterator))
        print(iterator.next(timeout=1))

