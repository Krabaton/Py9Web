class ValidPhoneException(Exception):
    pass


class PersonFormatterInfo:

    def value_of(self):
        raise NotImplementedError

# interface  PersonFormatterInfo:
#   value_of: def


class PersonAddress(PersonFormatterInfo):
    def __init__(self, city: str, street: str, house: int):
        self.city = city
        self.street = street
        self.house = house

    def value_of(self):
        return f"City: {self.city}, street: {self.street}, house: {self.house}"


class PersonPhoneNumber(PersonFormatterInfo):
    def __init__(self, phone: str, operator_code: str):
        if operator_code != "050":
            raise ValidPhoneException
        self.phone = phone
        self.operator_code = operator_code

    def value_of(self):
        return f"+38({self.operator_code}){self.phone}"


class Person:
    def __init__(self, name: str, phone: PersonFormatterInfo, address: PersonFormatterInfo):
        self.name = name
        self.phone = phone
        self.address = address

    def get_phone_number(self):
        return f"{self.name}: {self.phone.value_of()}"

    def get_address(self):
        return f"{self.name}: {self.address.value_of()}"


if __name__ == '__main__':

    # f = PersonFormatterInfo()
    # f.value_of()

    phone = PersonPhoneNumber("9995544", "050")
    address = PersonAddress("Kyiv", "Mazepa", 101)
    person = Person("Alexander", phone, address)
    print(person.get_phone_number())
    print(person.get_address())
