from typing import Union, TypeVar

Number = Union[float, int]

T = TypeVar("T", int, str, float)


def calculator(x: T, y: T) -> T:
    return x + y


print(calculator(3, 5))
print(calculator("Hello", "3"))
print(calculator(3.5, 1.5))


def add(x: Number, y: float | int) -> Number:
    return x + y
