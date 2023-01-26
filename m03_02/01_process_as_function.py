from multiprocessing import Process


def example_work(params):
    print(params)


if __name__ == '__main__':
    for i in range(5):
        pr = Process(target=example_work, args=(f"Count process - {i}",))
        pr.start()
