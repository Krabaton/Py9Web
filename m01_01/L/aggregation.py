class Animal:
    def __init__(self, nickname, age):
        self.nickname = nickname
        self.age = age

    def get_info(self):
        return f"It's an animal. His name is {self.nickname} and {self.age} years old"


class Owner:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def get_info(self):
        return f"{self.name} - {self.phone}"


class Cat(Animal):
    def __init__(self, nickname, age, owner: Owner):
        super().__init__(nickname, age)
        self.owner = owner

    def sound(self):
        return f"{self.nickname} say meow!"


if __name__ == '__main__':
    person = Owner('Denys', "0500019221")
    cat = Cat('Boris', 4, person)
    print(cat.owner.get_info())
