from threading import Thread


def worker(param):
    print(param)


if __name__ == '__main__':
    for i in range(5):
        th = Thread(target=worker, args=(f"Count thread - {i}", ))
        th.start()
