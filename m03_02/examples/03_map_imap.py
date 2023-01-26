from multiprocessing import Pool


def worker(val):
    return val ** 2


if __name__ == '__main__':

    with Pool(2) as pool:
        r = pool.map(worker, range(10))
        print(r)

        iterator = pool.imap(worker, range(10))
        print(iterator)
        for el in iterator:
            print(el)
