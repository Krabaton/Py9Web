from abc import ABC, abstractmethod
from enum import Enum


class OperationType(str, Enum):
    SUM = 'summary operation'
    MUL = 'mul'


class Operation(ABC):
    def __init__(self):
        self.data = None

    @abstractmethod
    def operation(self):
        pass

    @abstractmethod
    def info(self):
        ...


class Adder(Operation):
    def __init__(self, data_):
        self.data = data_

    def operation(self):
        return sum(self.data)

    def info(self):
        return OperationType.SUM.value


class Multiplier(Operation):
    def __init__(self, data_):
        self.data = data_

    def operation(self):
        mul = 1
        for el in self.data:
            mul *= el
        return mul

    def info(self):
        return OperationType.MUL.value


class Factory(ABC):
    @abstractmethod
    def create_operation(self):
        pass

    def make_operation(self):
        operation = self.create_operation()
        return operation


class MulFactory(Factory):
    def __init__(self, data_):
        self.data = data_

    def create_operation(self):
        return Multiplier(self.data)


class SumFactory(Factory):
    def __init__(self, data_):
        self.data = data_

    def create_operation(self):
        return Adder(self.data)


def calculation(factory):
    operator = factory.make_operation()
    return operator.operation(), operator.info()


if __name__ == '__main__':
    data = [1, 23, 4, 45, 23, 11]
    print(calculation(SumFactory(data)))
    print(calculation(MulFactory(data)))
