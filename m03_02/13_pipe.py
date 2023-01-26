from multiprocessing import Pipe, Process


class Foo:
    def __init__(self, value):
        self.value = value


def worker(receiver: Pipe):
    while True:
        instance = receiver.recv()
        print(f'All response: {instance}')
        if instance:
            print(f'Received: {instance}')
        else:
            return None


def main():
    start_pipe, end_pipe = Pipe()
    foo = Foo(100)
    my_worker = Process(target=worker, args=(end_pipe, ))
    my_worker.start()
    for el in [12, 'Hello world', {'year': 2022}, foo, foo.value, None]:
        start_pipe.send(el)


if __name__ == '__main__':
    main()



