from random import randint
from multiprocessing import Pool, current_process, cpu_count
from time import sleep, ctime


def worker():
    name = current_process().name
    print(f"Start process {name}: {ctime()}")
    r = randint(1, 3)  # Имитируем какую-то работу
    sleep(r)
    print(f"End work process {name}: {ctime()}")
    return f"Process{name} time run: {r} sec."


def callback(result):
    print(result)


if __name__ == "__main__":
    print(f"Count CPU: {cpu_count()}")
    with Pool(cpu_count()) as p:
        p.apply_async(worker, callback=callback)
        p.apply_async(worker, callback=callback)
        p.apply_async(worker, callback=callback)
        p.close()  # перестати виділяти процеси в пулл
        # p.terminate()  # убить всех
        p.join()  # дочекатися закінчення всіх процесів


    print(f"End {current_process().name}")

