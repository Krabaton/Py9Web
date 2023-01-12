class Car:
    def __init__(self):
        self._type = None

    def get_type(self):
        return self._type


class SportsCar(Car):
    def __init__(self):
        self._type = 'Sports car'


class FamilyCar(Car):
    def __init__(self):
        self._type = 'Family car'


class ECar(Car):
    def __init__(self):
        self._type = 'Electric car'


class FactoryCar:
    def __init__(self):
        self._cars = {}

    def register_car(self, car_type, car_class):
        self._cars[car_type] = car_class

    def create_car(self, car_type):
        if car_type in self._cars:
            return self._cars[car_type]()
        raise ValueError(f'Invalid cart type: {car_type}')


if __name__ == '__main__':
    #car = ECar()
    factory = FactoryCar()
    factory.register_car('sports', SportsCar)
    factory.register_car('family', FamilyCar)
    factory.register_car('electric', ECar)

    car = factory.create_car('electric')
    print(car.get_type())

