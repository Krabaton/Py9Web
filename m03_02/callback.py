def add(a, b):
    return a + b


def add_c(a, b, cb):  # Коли ми не знаємо скільки часу займе виконання
    r = a + b
    cb(r)
    return r


if __name__ == '__main__':
    r = add(2, 2)
    print(r)

    baz = add_c(2, 2, print)
    print(baz)
