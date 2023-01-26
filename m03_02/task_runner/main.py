import pathlib
from multiprocessing import Process, Queue, Event


class Concat:
    def __init__(self, output, event):
        self.work_order = Queue()
        self.event = event
        self.filename = output
        self.file = open(self.filename, 'w', encoding='utf-8')

    def __call__(self, *args, **kwargs):
        while True:
            if self.work_order.empty():
                if self.event.is_set():
                    print('Operation completed')
                    break
            else:
                reader_file, data = self.work_order.get()
                print(f'operation with file {reader_file.name}')
                self.file.write(f'{data}\n')

    def __getstate__(self):
        attributes = {**self.__dict__}
        attributes['file'] = None
        return attributes

    def __setstate__(self, value):
        self.__dict__ = value
        self.file = open(value['filename'], 'w', encoding='utf-8')

    def __del__(self):
        self.file.close()


def reader(work_queue, files_queue):
    while True:
        if files_queue.empty():
            break
        reader_file = files_queue.get()
        print(f'read file {reader_file.name}')
        with open(reader_file, 'r', encoding='utf-8') as fr:
            data = []
            for line in fr:
                data.append(line)
            data_all = ''.join(data)
            work_queue.put((reader_file, data_all))


if __name__ == '__main__':

    event_reader = Event()
    files_queue = Queue()

    list_files = pathlib.Path('.').joinpath('files').glob('*.js')

    for file in list_files:
        files_queue.put(file)

    if files_queue.empty():
        print('Folder is empty')
    else:
        source_file = 'main.js'
        concat = Concat(source_file, event_reader)
        process_concat = Process(target=concat, name='Concat')
        process_concat.start()

        processes = []
        for i in range(2):
            process_reader = Process(target=reader, args=(concat.work_order, files_queue), name=f'reader-{i}')
            processes.append(process_reader)
            process_reader.start()

        [process.join() for process in processes]
        event_reader.set()

