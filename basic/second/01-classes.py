#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Основы ООП - конструктор, наследование, перегрузка, полиморфизм, инкапсуляция
#
class User:
    first_name: str
    last_name:str

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def full_name(self):
        return f"Full name: {self.first_name} {self.last_name}" #formated string

class AgedUser(User):
    _age: int #protected
    """__age:int #private"""

    def __init__(self, first_name, last_name, age):
        super().__init__(first_name, last_name)
        self._age = age

agedJohn = AgedUser("John", "Doe", 30)

print(agedJohn.full_name(), agedJohn._age)