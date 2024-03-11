"""Модуль функцій роботи головної програми"""

import pickle
from datetime import datetime, timedelta
from address_book import Name, Phone, Birthday, Record, AddressBook
from file_manager import FileManager


# Декоратор
def input_error(func):
    """Декоратор опрацювання помилки при отримані данних з клавіатури"""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Неповні дані\n"
        except KeyError:
            return "Такий контакт відсутній\n"
        except IndexError:
            return "Індекс поза діапазоном\n"
        except NameError:
            return "Таке імʼя відсутнє в контактах"
        except AttributeError:
            return "Дані відсутні"

    return inner


# Функції
def get_menu_from_file(path):
    """Отримання і формування меню з файлу - повертає словник"""
    menu = {}
    with FileManager(path) as fh:
        # with open(path, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()
    for line in lines:
        cmd, action = line.strip().split(
            ",", 1
        )  # Розбиття на елементи за заданим розділювачем
        menu[cmd] = action
    return menu


def get_data_from_file(path):
    """Отримання і формування контактів з файлу - повертає AddressBook"""
    try:
        with FileManager(path, mode="rb", encoding=None) as fh:
            return pickle.load(fh)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


# Збереження контактів у файл у випадку зміни
def rewrite_contacts(book: AddressBook, path="addressbook.pkl"):
    """Перезапис контактів у файл перед закриттям програми"""
    with FileManager(path, mode="wb", encoding=None) as fh:
        pickle.dump(book, fh)
    print("Контакти оновлено")


# Виведення основого меню
def print_menu(menu):
    """Друк меню"""
    print()
    title = "Меню"
    print(f"{title:^30}")
    for k, v in menu.items():
        print(f"{k:<35}{v:<25}")
    print()


# Функція парсеру команд
@input_error
def parse_input(user_input):
    """Розбиття введених даних на команду та аргументи"""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Функції обробки команд - handlers
def print_contacts(contacts: AddressBook):
    """Друк контактів"""
    print(contacts.get_book())


@input_error
def show_contact(args, contacts: AddressBook):
    """Виводить контакт книги за ім'ям"""
    name = args[0]
    rec_find = contacts.find_record(name)
    if rec_find:
        return rec_find
    raise KeyError


@input_error
def add_contact(args, contacts: AddressBook):
    """Додає контакт до книги за ім'ям"""
    name, phone = args
    rec_find = contacts.find_record(name)
    if rec_find:
        phone = Phone(phone)
        rec_find.add_phone(phone)
        contacts.add_record(rec_find)
        return f"Існуєчий контакт {name} оновлено\n"
    name = Name(name)
    phone = Phone(phone)
    new_record = Record(name)
    new_record.add_phone(phone)
    contacts.add_record(new_record)
    return f"Контакт {name} додано"


@input_error
def change_contact(args, contacts: AddressBook):
    """Змінює контакт книги за ім'ям"""
    name, phone = args
    phone = Phone(phone)
    if phone.value:
        rec_find = contacts.find_record(name)
        if rec_find:
            rec_find.edit_phone(rec_find.phones[0].value, phone.value)
            return f"Контакт {name} змінено.\n"
    return "Невірно введений номер телефону"


@input_error
def del_contact(args, contacts: AddressBook):
    """Видаляє контакт книги за ім'ям"""
    name = args[0]
    contacts.del_record(name)
    return f"Контакт {name} видалено\n"


@input_error
def show_birthday(args, contacts: AddressBook):
    """Виводить день народження з книги за ім'ям"""
    name = args[0]
    rec_find = contacts.find_record(name)
    return rec_find.birthday.value.strftime("%d-%m-%Y")


@input_error
def birthdays(contacts: AddressBook):
    """Виводить дні народження з книги на найближчий тиждень від сьогодні"""
    today = datetime.today().date()
    congratulation_list = []

    for user in contacts.data.items():
        if user[1].birthday:
            congratulation_user_dict = {}
            dict_keys = ("Ім'я", "Дата привітання")
            user_birthday = user[1].birthday.value
            if user_birthday:
                birthday_this_year = datetime(
                    year=today.year, month=user_birthday.month, day=user_birthday.day
                ).date()

                if birthday_this_year < today:
                    continue
                elif birthday_this_year.toordinal() - today.toordinal() > 7:
                    continue
                else:
                    congratulation_date = datetime(
                        year=today.year,
                        month=birthday_this_year.month,
                        day=birthday_this_year.day,
                    ).date()
                    if congratulation_date.weekday() == 6:
                        congratulation_date += timedelta(days=1)
                    elif congratulation_date.weekday() == 5:
                        congratulation_date += timedelta(days=2)

                    congratulation_date = congratulation_date.strftime("%Y-%m-%d")
                    congratulation_user_dict.update(
                        {dict_keys[0]: user[1].name, dict_keys[1]: congratulation_date}
                    )
                    congratulation_list.append(congratulation_user_dict)
    if congratulation_list:
        return "\n".join(map(str, congratulation_list))
    return "Не знайдено коистувачів у кого ДН на цьому тижні"


@input_error
def add_birthday(args, contacts: AddressBook):
    """Додати день народження в книги за ім'ям"""
    name = args[0]
    birthday = args[1]
    rec_find = contacts.find_record(name)
    if rec_find:
        rec_find.add_birthday(Birthday(birthday))
        print(f"Для контакту {name} оновлено дату дня народження на {birthday}")
