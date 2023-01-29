# Пояснення

## 01_process_as_function.py

```python
from multiprocessing import Process


def example_work(params):
    print(params)


if __name__ == '__main__':
    for i in range(5):
        pr = Process(target=example_work, args=(f"Count process - {i}",))
        pr.start()
```

Це базовий приклад використання багатопроцесорного модуля в Python для створення кількох процесів.
Клас `Process` з модуля `multiprocessing` використовується для створення нового процесу. Цільовий параметр
встановлюється на функцію, яку слід запустити в новому процесі (у цьому випадку функція `example_work`), а
параметр `args` встановлюється як кортеж аргументів, які слід передати функції (у цьому випадку це a рядок, що містить
кількість процесів).

У блоці `if __name__ == '__main__':` використовується цикл для створення 5 нових процесів за допомогою класу `Process`.
Кожного разу під час проходження циклу викликається метод `pr.start()`, щоб запустити новий процес.

Функція `example_work` приймає один аргумент під назвою `params` і друкує його в консолі.

Таким ином буде створено 5 процесів, і кожен процес запустить функцію `example_work` із переданим параметром `"Count
process - i"`.

## 02_process__as_class.py

```python
from multiprocessing import Process


class MyProcess(Process):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        self.kwargs.get('log')(f"args: {self.args}")


def log(msg):
    print(msg)


if __name__ == '__main__':
    for i in range(5):
        pr = MyProcess(args=(f"Count Process - {i}",), kwargs={'log': log})
        pr.start()
```

Цей код подібний до попереднього прикладу, але він використовує спеціальний клас `Process` під назвою `MyProcess`,
який успадковує клас `Process` багатопроцесорного модуля. Цей спеціальний клас замінює конструктор `__init__` і метод
запуску `run`.

У спеціальному методі `__init__` виклик `super().__init__` використовується для виклику конструктора батьківського
класу, і
він встановлює властивості `args` і `kwargs` для об’єкта для використання в методі `run`.

Таким чином, кінцевим результатом буде 5 процесів, що виконуються одночасно з різними параметрами та викликають функцію
журналу для друку повідомлення.

## 03_process__join.py

```python
from multiprocessing import Process
from time import sleep


def example_work(params):
    sleep(0.5)
    print(params)


if __name__ == '__main__':
    prs = []
    for i in range(5):
        pr = Process(target=example_work, args=(f"Count process - {i}",))  # daemon=True
        pr.start()
        prs.append(pr)

    [el.join() for el in prs]

    print('End program')
```

Цикл створює 5 нових процесів за допомогою класу `Process`, як і в попередніх прикладах. Цільовий параметр `target`
встановлюється на функцію, яку слід запустити в новому процесі (функція `example_work`), а параметр `args`
кортеж аргументів, які слід передати функції.

Функція `example_work` приймає один аргумент під назвою `params` і викликає функцію `sleep(0.5)` перед тим, як вивести
його в консоль. Ця функція переведе поточний потік у режим сну на вказаний час у секундах.

Потім кожен процес додається до списку `prs` і викликається метод `pr.start()` для запуску нового процесу.

Після циклу `[el.join() for el in prs]` чекатиме завершення всіх процесів, перш ніж програма продовжить роботу. Метод
`join()` блокує виконання основного процесу, доки не завершиться процес, чий метод `join()` викликається.

Нарешті, програма друкує на консолі «End program», вказуючи, що всі процеси завершено, і програма завершена.

## 04_process_lock_value_array.py

```python
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
```

У цьому прикладі `POOL_SIZE = 5` визначає кількість потоків. Далі ми створюємо спільний лічильник об’єкта `Value`, тобто
ціле число, яке ініціалізується значенням `0`, визнааєм блокування об’єкта `RLock` і масив об’єктів `Array`, який є
спільним масивом цілих чисел довжиною `POOL_SIZE`.

В циклі створюємо 5 нових процесів за допомогою класу `Process`, як і
в попередніх прикладах.

Функція `example_work` приймає 4 аргументи, `counter, lock, arr, index`, і виконується в нескінченному циклі. У циклі
вона отримує блокування та збільшує значення спільного лічильника на `1`. Потім призначає значення `counter` індексу
спільного масиву, а потім робить поточний потік сплячим на випадкову кількість секунд від `1` до `2`. Потім відкриває
файл `"result.txt"` у режимі додавання та записує значення лічильника, після якого йде новий рядок `\n`.

Після циклу програма засинає на `3` секунди. Потім вона друкує спільний масив і, нарешті, друкує на консолі «End
program», вказуючи, що всі процеси завершено та програму завершено.

Таким чином, кінцевим виходом буде `5` процесів, що виконуються одночасно в нескінченному циклі та збільшують спільний
лічильник `Value` і масив `Array`, а також записують значення лічильника у файл `result.txt`.

## value_array.py

```python
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

```

Цей сценарій використовує багатопроцесорний модуль для створення трьох окремих процесів. Кожен процес запускає робочу
функцію, яка приймає три спільні змінні: значення `Value`, масив `Array` і масив `Array` точки `Point`.

`RLock` — це клас у багатопроцесорному модулі, який використовується для створення блокування,
який можна використовувати для синхронізації доступу до спільних ресурсів між різними процесами.
Змінна блокування `lock`, яка є екземпляром `RLock`, передається як параметр блокування, щоб забезпечити синхронізацію
доступу до спільного значення між різними процесами.

Робоча функція `worker` спочатку збільшує значення об’єкта `Value` на `1`, а потім друкує поточне значення разом із
назвою процесу.
Потім він перетворює рядок у верхній регістр, виконує ітерацію по масиву об’єктів `Point` і збільшує поля `x` і `y`
кожної точки на поточне значення.

Потім сценарій створює та запускає три окремі процеси, передаючи спільні змінні як аргументи робочій функції. Після
запуску всіх процесів він чекає їх завершення за допомогою методу `join()`, а потім друкує код виходу кожного процесу та
остаточні значення спільних змінних.

Оператор `exit(0)` наприкінці робочої функції вийде з робочого процесу з кодом стану `0`, що вказує на успішне
завершення.

## 05_process_event.py

```python
from multiprocessing import Process, Event
from time import sleep


def example_work(event: Event):
    print("Run event work")
    event.wait()
    print("Flag event is true")


def example_work_timeout(event: Event, time: float):
    while not event.is_set():
        print("Wait until the event flag is set")
        event_wait = event.wait(time)
        print("Has our flag been set?")
        if event_wait:
            print("We start working on a signal")
        else:
            print("Still waiting until the event flag is set")


if __name__ == "__main__":
    event = Event()
    pr = Process(target=example_work, args=(event,))
    pr.start()

    pr_timeout = Process(target=example_work_timeout, args=(event, 1))
    pr_timeout.start()

    sleep(5)
    event.set()

    print("End program")
```

Цей код демонструє використання класу `Event` із багатопроцесорного модуля. Подія — це примітив синхронізації, який
можна використовувати для сигналізації між процесами.

У цьому коді є дві функції `example_work` і `example_work_timeout`. Перша функція, `example_work`, приймає
об’єкт `Event` як аргумент і запускає цикл, який очікує встановлення події. Коли подія встановлена, вона друкує "Flag
event is true" та продовжує виконання.

Друга функція, `example_work_timeout`, також приймає об’єкт `Event` як аргумент, а також час у секундах. Він запускає
цикл,
який очікує, поки подія не буде встановлена, використовуючи метод `wait()` з аргументом `time`. Якщо подія встановлена,
друкується "We start working on a signal" і продовжується виконання. Якщо час закінчується, а події немає, то друкується
"Still waiting until the event flag is set".

Наприкінці сценарію створюється об’єкт `Event` і запускаються два процеси: один виконує `example_work`, а інший —
`example_work_timeout`. Потім основний процес перебуває в режимі сну на `5` секунд, протягом якого подія не
встановлюється.
Через `5` секунд головний процес встановлює подію, яка змушує два процеси припинити очікування та продовжити виконання.
Нарешті, програма завершується і друкує "End program".

## 06_event_stop.py

```python
from multiprocessing import Process, Event
from time import sleep


def example_work(event_for_exit: Event):
    while True:
        sleep(1)
        print('Run event work')

        if event_for_exit.is_set():
            break


if __name__ == '__main__':
    event = Event()
    pr = Process(target=example_work, args=(event,))
    pr.start()

    sleep(5)
    event.set()

    print('End program')
```

Цей код створює процес за допомогою класу `Process` з багатопроцесорного модуля. Функція `example_work` передається як
ціль
процесу, і їй передається об’єкт `Event` під назвою `event_for_exit`. Усередині функції створюється нескінченний цикл за
допомогою оператора `while True`. У межах циклу функція спить на одну секунду, друкує 'Run event work', а потім
перевіряє стан об’єкта події, викликаючи метод `is_set()`.

Якщо метод `is_set()` повертає `True`, цикл розривається, і функція завершує роботу. Якщо метод `is_set()` повертає
значення `False`, цикл продовжується, і процес перебуває в режимі сну ще на одну секунду, перш ніж знову друкувати 'Run
event work'.

У блоці `main`: створюється екземпляр класу `Event`, який передається як аргумент функції `example_work`
під час запуску процесу. Потім основний процес перебуває в режимі сну на `5` секунд, після чого встановлює позначку
події за допомогою методу `set()`. Це призведе до переривання нескінченного циклу в процесі `example_work`, і процес
завершиться.
Нарешті, програма друкує 'End program', щоб вказати, що основний процес завершено.

## 07_event_restart.py

```python
from multiprocessing import Process, Event
from time import sleep


def example_work(event_for_exit: Event):
    while True:
        sleep(1)
        if event_for_exit.is_set():
            continue
        else:
            print('Run event work')


if __name__ == '__main__':
    event = Event()
    pr = Process(target=example_work, args=(event,), daemon=True)
    pr.start()
    print('Start!')
    sleep(3)
    print('Stop!')
    event.set()
    sleep(3)
    print('Start!')
    event.clear()
    sleep(3)
    print('Stop!')
    event.set()
    print('End program')
```

Цей код створює процес під назвою `pr`, який запускає функцію `example_work` і передає об’єкт `Event` як аргумент.
Функція `example_work` входить у нескінченний цикл і засинає на `1` секунду на кожній ітерації. Усередині циклу функція
перевіряє, чи встановлено `event_for_exit`. Якщо це так, функція продовжує до наступної ітерації `continue`, інакше вона
запускає повідомлення 'Run event work'.

Потім батьківський процес запускає дочірній процес і встановлює `event_for_exit` через `3` секунди, що
змушує дочірній процес припиняти друк повідомлення 'Run event work'.

Потім він очищає подію `event.clear()` ще через 3 секунди, що змушує дочірній процес знову почати друкувати 'Run event
work'. Потім він знову встановлює подію ще через 3 секунди, змушуючи дочірній процес припинити друк повідомлення.
Нарешті, батьківський процес друкує print('End program') та завершує роботу.

Параметр `daemon=True` робить процес демоном, що означає, що він автоматично завершить роботу, коли завершиться вихід
основного процесу.

## 08_condition.py

```python
from multiprocessing import Process, Condition
from time import sleep


def worker(condition: Condition):
    print("Run event work")
    with condition:
        condition.wait()
        print("The owner gave Doby a sock! Can work")


def master(condition: Condition):
    print("Master does the hard work")
    with condition:
        print("We give permission for others to work")
        condition.notify_all()


if __name__ == "__main__":
    condition = Condition()
    master_one = Process(name="master", target=master, args=(condition,))

    worker_one = Process(target=worker, args=(condition,))
    worker_two = Process(target=worker, args=(condition,))
    worker_one.start()
    worker_two.start()

    sleep(5)
    master_one.start()

    print("End program")
```

Цей код використовує багатопроцесорний модуль для створення двох процесів, один з яких називається `master`, а два
інших — `worker`. Клас `Condition` з багатопроцесорного модуля використовується для синхронізації двох процесів.

У робочому процесі `worker` викликає метод `wait()` об’єкта умови, який змушує процес чекати, доки метод `notify_all()`
не буде викликано для об’єкта умови головним процесом `master`. Потім робочий процес друкує "The owner gave Doby a sock!
Can work"

У головному процесі `master` виконує певну «важку роботу»: "Master does the hard work", а потім викликає метод
`notify_all()` для об’єкта умови, який активує всі робочі процеси, які очікують на об’єкт умови, дозволяючи їм
продовжити виконання. Потім головний процес друкує "We give permission for others to work".

У основній функції створюється об’єкт умови `Condition`, а також створюються та запускаються головний і робочий процеси.
Робочі процеси запускаються першими та негайно викликають метод `wait()`, переводячи їх у стан очікування. Потім
основний потік засинає на `5` секунд і запускає головний процес, який виконує свою важку роботу, а потім викликає метод
`notify_all`, який пробуджує робочі процеси, дозволяючи їм продовжити виконання та надрукувати "The owner gave Doby a
sock! Can work".

## 09_semaphore_manager.py

```python
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
```

Цей код демонструє використання семафора в багатопроцесному середовищі. Семафор — це об’єкт синхронізації, який керує
доступом кількох процесів до спільного ресурсу в середовищі паралельного програмування.

Тут клас `Semaphore` імпортується з багатопроцесорного модуля, і створюється об’єкт семафора з початковим значенням `3`.
Визначається робоча функція `worker`, яка приймає об’єкт семафор і словник як аргументи. Усередині функції він спочатку
очікує, поки семафор буде звільнений іншими процесами. Потім він друкує назву процесу, імітує певну роботу, перебуваючи
в режимі сну протягом випадкової тривалості, і зберігає цю тривалість у словнику.

У блоці `main` об'єкт `Manager` використовується для створення спільного словника `result`, в результаті чого всі
процеси мають до нього доступ. Створюється та запускається `10` процесів, кожен з яких має унікальне ім’я, і всі вони
передають однакові об’єкти семафора та словника робочій функції. Метод `join` викликається для кожного процесу, який
очікує завершення процесу. Нарешті друкується зміст словника.

Семафор обмежує кількість процесів, які можуть отримати семафор і виконати критичну частину коду за раз. Тут семафор
ініціалізується значенням `3`, що означає, що максимум `3` процеси можуть отримати семафор і виконати критичну частину
коду одночасно. Інструкція `with semaphore`: використовується для отримання семафора та виконання критичної частини
коду. Після завершення виконання коду всередині блоку семафор автоматично звільняється.

## 10_barrier.py

```python
from random import randint
from multiprocessing import Process, Barrier, current_process
from time import sleep, ctime


def worker(barrier: Barrier):
    name = current_process().name
    print(f"Start thread {name}: {ctime()}")
    sleep(randint(1, 3))  # Имитируем какую-то работу
    barrier.wait()
    print(f"Barrier crossed for {name}")
    print(f"End work thread {name}: {ctime()}")


if __name__ == "__main__":

    barrier = Barrier(5)

    for num in range(10):
        pr = Process(name=f"Process-{num}", target=worker, args=(barrier,))
        pr.start()

    print("End program")
```

Цей код створює об’єкт `Barrier` зі значенням `5`, що означає, що `5` робочих процесів повинні
викликати `barrier.wait()`, перш ніж будь-який із них зможе продовжити роботу. Потім створюється та виконується
одночасно 10 робочих процесів. Кожен робочий процес імітує певну роботу, перебуваючи в режимі сну на випадковий проміжок
часу від 1 до 3 секунд, а потім викликає `barrier.wait()`. Після того, як `5` робочих процесів
викличуть `barrier.wait()`, усі вони зможуть продовжити роботу та друкують повідомлення про те, що вони перетнули
бар’єр. Потім процес завершується, друкуючись оператор "End work thread". Остаточним результатом буде випадковий
порядок початку та завершення кожного процесу, але всі вони чекатимуть, поки `5` з них перетнуть бар’єр.

## 11_pool.py

```python
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
```

Цей сценарій створює багатопроцесорний пул із кількістю робочих процесів, що дорівнює кількості CPU, доступних на
машині. Робоча функція `worker` імітує певну роботу, затримуючи випадкову кількість секунд, а потім повертає рядок, що
містить назву процесу та час, який знадобився для завершення роботи. Потім сценарій застосовує робочу функцію асинхронно
3 рази та встановлює функцію зворотного виклику для друку результату кожної робочої функції. Сценарій також закриває
пул, щоб більше не можна було додавати робочі процеси, а потім очікує завершення всіх робочих процесів перед виходом.
Наприкінці сценарію буде надруковано ім’я основного процесу, яким є "MainProcess".

## 12_pool_map.py

```python
from multiprocessing import Pool, current_process, cpu_count


def worker(n):
    sum = 0
    for i in range(n):
        sum += i
    return sum


def callback(result):
    print(f"Result in callback: {result}")


if __name__ == "__main__":
    print(f"Count CPU: {cpu_count()}")
    with Pool(cpu_count()) as p:
        p.map_async(
            worker,
            [100, 200, 1024, 10, 23, 2314, 34, 24, 242, 24, 12, 2222, 3333, 444, 55],
            callback=callback,
        )
        p.close()  # перестати виділяти процеси в пулл
        p.join()  # дочекатися закінчення всіх процесів
```

Код створює пул робочих процесів із кількістю робочих процесів, яка дорівнює кількості ядер CPU у системі. Метод
`map_async` використовується для застосування робочої функції до списку аргументів. Функція зворотного
виклику `callback` викликається після завершення робочої функції, і вона друкує результат робочої функції. Метод `close`
викликається, щоб припинити призначення нових процесів пулу, а метод `join` викликається, щоб очікувати завершення всіх
робочих процесів.

Цей код виконає підсумовування чисел від `0` до `n` для кожного числа в наданому списку та надрукує результат у функції
зворотного виклику `callback`.

## 13_pipe.py

```python
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
    my_worker = Process(target=worker, args=(end_pipe,))
    my_worker.start()
    for el in [12, 'Hello world', {'year': 2022}, foo, foo.value, None]:
        start_pipe.send(el)


if __name__ == '__main__':
    main()
```

Цей сценарій створює клас `Foo` з одним значенням атрибута та робочу функцію, яка виконується в окремому процесі та
отримує об’єкти через канал `Pipe`. Основна функція створює екземпляр `Foo` та процес, який запускає робочу функцію,
`worker` передаючи кінець каналу як аргумент. Потім основна функція надсилає декілька різних типів об’єктів через канал
до робочого процесу, який отримує їх і друкує. Робочий процес `worker` продовжує отримувати об’єкти, доки не буде
отримано об’єкт `None`, після чого він повертає `None` і виходить із циклу.

## 14_pipe_duplex.py

```python
from multiprocessing import Pipe, Process


class Foo:
    def __init__(self, value):
        self.value = value


def worker(receiver: Pipe):
    while True:
        try:
            instance = receiver.recv()
            receiver.send(f'Ok for: {instance}')
            print(f'Received: {instance}')
        except EOFError:
            return None


def wk(sender: Pipe, store):
    for el in store:
        sender.send(el)
        print(sender.recv())


def main():
    start_pipe, end_pipe = Pipe()
    foo = Foo(100)
    store = [12, 'Hello world', {'year': 2022}, foo, foo.value, 42, None, 43]
    my_worker = Process(target=worker, args=(end_pipe,))
    my_wk = Process(target=wk, args=(start_pipe, store))
    my_worker.start()
    my_wk.start()

    my_wk.join()
    start_pipe.close()
    end_pipe.close()


if __name__ == '__main__':
    main()
```

Наведений вище код створює два процеси, один називається `my_worker`, а інший — `my_wk`. Процес `my_worker` запускає
робочу функцію, яка отримує об’єкт `Pipe` як аргумент і входить у цикл `while`. У циклі `while` він постійно отримує
об’єкти з каналу та друкує їх. І навіть якщо отриманий об’єкт `None`, функція його повертає.

Процес `my_wk` запускає функцію `wk`, яка також отримує об’єкт `Pipe` і список об’єктів для надсилання як аргументів.
Функція `wk` повторює список і надсилає кожен об’єкт через канал і отримує відповідь від робочої функції `worker`.

У основній функції два канали створюються за допомогою функції `Pipe`, і ці канали передаються до процесів `my_worker` і
`my_wk` відповідно. Визначається клас `Foo`, і екземпляр цього класу створюється та додається до списку об’єктів, які
надсилаються через канал. Запускаємо два процеси, `my_worker` і `my_wk`, і гарантуємо, що вони завершили
своє виконання перед завершенням програми `my_wk.join()`.

## 02_work_file_test.py

Цей код демонструє використання багатопоточності та багатопроцесорності в Python. Він обчислює квадрат кожного числа в
заданому діапазоні значень і записує результат у файл.

У цьому коді використовується клас `Thread` із модуля `threading` для створення трьох потоків, кожен з яких виконує
обчислення для іншої підмножини значень. Блокування використовується для запобігання умов змагання під час запису
результатів у файл. Вимірюється та друкується час, необхідний потокам для завершення обчислення.

Потім у коді використовується клас `Process` із модуля багатопроцесорності, щоб створити три процеси, кожен з яких
виконує обчислення для іншої підмножини значень. Блокування використовується для запобігання умов змагання під час
запису результатів у файл. Вимірюється та друкується час, необхідний процесам для завершення обчислення.

Потім код використовує той самий єдиний процес для виконання обчислення значень, а витрачений час вимірюється та
друкується.

Нарешті, у коді використовується клас `Pool` із модуля `multiprocessing.dummy` для створення пулу з трьох робочих
потоків, кожен з яких виконує обчислення для іншої підмножини значень. Блокування використовується для запобігання умов
змагання під час запису результатів у файл. Вимірюється та друкується час, необхідний робочим потокам для завершення
обчислення.

Важливо відзначити, що клас `Pool` із модуля `multiprocessing.dummy` створює потоки замість процесів, це корисно у
випадках, коли накладні витрати на створення нового процесу занадто високі, але функція не є потокобезпечною.

## 05_pipe.py

```python
from multiprocessing import Process, Pipe
from time import sleep
import sys


def worker(conn: Pipe, name):
    print(f'{name} started!')
    val = conn.recv()
    print(f'{name} {val ** 2}')
    sys.exit(0)  # Если не ноль, то это код ошибки


if __name__ == '__main__':
    rcv1, snd1 = Pipe(duplex=False)
    rcv2, snd2 = Pipe(duplex=False)

    pr1 = Process(target=worker, args=(rcv1, 'first'))
    pr2 = Process(target=worker, args=(rcv2, 'second'))

    pr1.start()
    pr2.start()

    snd1.send(10)
    sleep(2)
    snd2.send(5)

```

Цей код створює два окремих процеси `pr1` і `pr2`, які запускаються функцією `worker`. Кожен процес передається
екземпляру `pipe` як перший аргумент і рядком за назвою процесу: 'перший' або 'second'.

Два екземпляри `pipe` `rcv1` і `rcv2` використовуються процесами для отримання даних від основного процесу. Екземпляри
`pipe` `snd1` і `snd2` використовуються основним процесом для передачі даних процесам.

Після старту процесів основний процес посилає 10 на перший процес
використовуючи `snd1.send(10)` і чекає 2 секунди, використовуючи `sleep(2)`. Нарешті, основний процес посилає 5 на
другий
процес використовуючи `snd2.send(5)`.

У кожному з двох процесів значення, отримане від основного процесу, зводиться в квадрат і друкується. Нарешті, процес
завершується з кодом виходу 0, що вказує на його успішне завершення.

## 06_queue.py

```python
from multiprocessing import Process, Queue
from time import sleep
import sys


def worker(qu: Queue, name):
    print(f"{name} started!")
    val = qu.get()
    print(f"{name} {val ** 2}")
    sys.exit(0)  # Если не ноль, то это код ошибки


if __name__ == "__main__":
    qu = Queue()

    pr1 = Process(target=worker, args=(qu, "first"))
    pr2 = Process(target=worker, args=(qu, "second"))

    pr1.start()
    pr2.start()

    qu.put(10)
    sleep(2)
    qu.put(5)
    qu.put(15)  # ніхто мене не лове
```

Код створює два процеси, `pr1` і `pr2`, і запускає їх. Процеси отримують чергу `qu` як параметр і чекають, поки значення
будуть розміщені в черзі. Потім головний процес поміщає в чергу три значення: `10`, `5` і `15`. Робоча функція `worker`
отримує значення з черги та обчислює квадрат значення. Тоді квадрат друкується разом із назвою процесу. Оскільки існує
два процеси, кожен процес отримає різне значення з черги та виконає обчислення. Зверніть увагу, що третє значення `15`
не витягується з черги, оскільки другий процес уже завершив роботу.

## 07_joinqueue.py

```python
from multiprocessing import Process, JoinableQueue
from time import sleep
import sys


def worker(qu: JoinableQueue, name):
    print(f'{name} started!')
    val = qu.get()
    print(f'{name} {val ** 2}')
    sleep(2)
    qu.task_done()
    sys.exit(0)  # Если не ноль, то это код ошибки


if __name__ == '__main__':
    qu = JoinableQueue()

    pr1 = Process(target=worker, args=(qu, 'first'))
    pr2 = Process(target=worker, args=(qu, 'second'))

    pr1.start()
    pr2.start()

    qu.put(10)
    sleep(2)
    qu.put(5)
    qu.join()
    print('Finished')
```

Код створює два дочірні процеси, 'first' і 'second', використовуючи клас `Process` з багатопроцесорного модуля. Дочірні
процеси отримують об’єкт `JoinableQueue`, `qu`, як аргумент і запускають робочу функцію `worker`.

Робоча функція `worker` отримує значення з черги за допомогою `qu.get()` і друкує квадрат цього значення. Потім він
чекає 2 секунди за допомогою `sleep(2)` і позначає завдання як виконане за допомогою `qu.task_done()`. Потім дочірній
процес завершує роботу з кодом 0.

У головному процесі запускаються два дочірніх процеси, 'first' і 'second', і значення `10` і `5` додаються до черги.
Потім головний процес блокується на `qu.join()`, очікуючи, поки всі завдання будуть позначені як виконані. Коли всі
завдання виконані, виводиться повідомлення «Finished», і основний процес продовжує своє виконання.

## file_sort/main_map.py

Програма реалізує завдання сортування папок. За наявності вихідної папки він рекурсивно читає вміст папки та
її вкладених папок і копіює всі файли в новій папці за їхнім розширенням. За замовчуванням вихідна папка є "dist", і її
можна змінити за допомогою параметра "--output". Програма використовує бібліотеку `argparse` для аналізу аргументів
командного рядка, бібліотеку `pathlib` для обробки шляхів і каталогів, бібліотеку `shutil` для копіювання файлів і
багатопроцесорну бібліотеку для одночасного копіювання файлів.

## task_runner/main.py

Цей сценарій реалізує рішення для об’єднання кількох файлів `.js` у каталозі `files` в один файл. Сценарій використовує
бібліотеку `Pathlib` для пошуку файлів `.js`, а також черги та події із багатопроцесорного модуля для взаємодії між
процесами.

Клас `Concat` забезпечує основну функціональність конкатенації. Він записує вміст кожного файлу `.js` у цільовий файл
`main.js`, використовуючи метод запису файлового об’єкта. Клас `Concat` також реалізує методи серіалізації `getstate`,
`setstate`, щоб забезпечити міжпроцесний зв’язок між процесами читання та процесом конкатенації.

Функція `reader` зчитує вміст кожного файлу `.js` і надсилає його екземпляру `Concat` через чергу `work_order`. Функція
`reader` продовжує цикл і читає вміст файлів, доки `files_queue` не буде порожнім.

Основна функція встановлює необхідний міжпроцесний зв’язок і запускає 2 процеси читання та процес `Concat`. Процеси
читання зчитують вміст файлів `.js` і надсилають його процесу `Concat` через чергу `work_order`. Процес `Concat`
продовжує записувати вміст файлів `.js` у файл `main.js`, доки не буде встановлено `event_reader`, що вказує на те, що
всі файли оброблено. Потім процеси `[process.join() for process in processes]` в очікуванні їх завершення. А значить
прийшов час встановити `event_reader`.