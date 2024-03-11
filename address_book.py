"""Система управління адресною книгою"""

from collections import UserDict
from datetime import datetime
import re


# Клас базовий поля - запису
class Field:
    """Базовий клас Поля"""

    def __init__(self, value=""):
        self.value = value

    def __repr__(self):
        return f"{self.value}"

    def set_value(self, value: str):
        """Присвоїти значення"""
        self.value = value


class Name(Field):
    """Клас для зберігання імені контакту"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Phone(Field):
    """Клас для зберігання одиничного номера, з приведенням до стандартного типу"""

    def __init__(self, value: str):
        if len(value) == 10 and re.search(r"\d{10}", value):
            self.value = value
        else:
            self.value = None

    def set_value(self, value: str):
        if len(value) == 10 and re.search(r"\d{10}", value):
            self.value = value
        else:
            self.value = None


class Birthday(Field):
    """Клас для зберігання дати народження"""

    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            print(f"Помилка вводу: {ValueError}")
            self.value = None
            raise ValueError("Некоректний формат дати. Має бути ДД.ММ.РРРР")


class Record:
    """Клас для зберігання інформації про контакт,
    включаючи ім'я, список телефонів та день народження"""

    def __init__(self, name):
        self.name = name
        self.phones = []
        self.birthday = None

    def __repr__(self):
        if self.birthday:
            return f"Ім'я контакту: {self.name.value}, Дата народження: {self.birthday.value} \
Телефонні номери: {'; '.join(p.value for p in self.phones)}"
        return f"Ім'я контакту: {self.name.value}, \
Телефонні номери: {'; '.join(p.value for p in self.phones)}"

    # Робота з полем Ім'я
    def get_name(self):
        """Отримати значення імені"""
        return f'"{self.name.value}"'

    # Робота з полем Номер Телефону
    def find_phone(self, phone: Phone):
        """Знайти телефон"""
        i = -1
        for p in self.phones:
            i += 1
            if phone.value == p.value:
                return (True, i)
            else:
                continue
        return (False, -1)

    def add_phone(self, phone: Phone):
        """Додати телефон"""
        if phone.value and not self.find_phone(phone)[0]:
            self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        """Видалити телефон"""
        if self.find_phone(phone)[0]:
            self.phones.remove(phone)

    def edit_phone(self, value_old: str, value_new: str):
        "Змінити телефон"
        phone_old = Phone(value_old)
        phone_new = Phone(value_new)
        if phone_new:
            is_phone_old, i = self.find_phone(phone_old)
            is_phone_new = self.find_phone(phone_new)
            if not is_phone_new and is_phone_old:
                self.phones[i] = phone_new

    # Робота з полем День народження
    def add_birthday(self, birtday: Birthday):
        """Додати/Змінити дату дня народження"""
        if birtday.value:
            self.birthday = birtday


class AddressBook(UserDict):
    """Клас для зберігання та управління записами"""

    def get_book(self):
        """Отримати всю книгу записів"""
        tytles = ("Name", "Tel", "Birthday")
        form_factor = 12
        t1 = f"{tytles[0]:<{form_factor}}"
        t2 = f"{tytles[1]:<{form_factor*2}}"
        t3 = f"{tytles[2]:<{form_factor}}"
        string = "|" + t1 + "|" + t2 + "|" + t3 + "|\n"
        string += "-" * len(string) + "\n"
        for k in self.data.items():
            st1 = f"{k[0].value:<{form_factor}}"
            st2 = f'{"; ".join(p.value for p in k[1].phones):<{form_factor*2}}'
            st3 = f"{str(k[1].birthday):<{form_factor}}"
            string += "|" + st1 + "|" + st2 + "|" + st3 + "|\n"
        return string

    def add_record(self, record: Record):
        """Додати запис до книги"""
        key = record.name
        self.data[key] = record

    def find_record(self, name: str):
        """Знайти запис у книзі"""
        for k in self.data.items():
            if k[0].value == name:
                return k[1]
            else:
                continue
        return None

    def del_record(self, name: str):
        """Видалити запис"""
        del_rec = None
        for k in self.data.items():
            if k[0].value == name:
                del_rec = k[1]
                break
            else:
                continue
        if del_rec:
            self.data.pop(del_rec.name)
        return "Успішно" if del_rec else "Запис відсутній"
