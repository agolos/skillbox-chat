#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Основы ООП, класс, объект, метод и атрибут
#
class User:
    first_name: str
    last_name:str

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def full_name(self):
        return f"Full name: {self.first_name} {self.last_name}" #formated string

john = User("John", "Doe")
print(john.full_name())