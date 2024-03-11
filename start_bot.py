"""Головний код запуску бота"""

from pathlib import Path
from style import print_tytle, print_end, log_error
from cli_bot_func import (
    get_data_from_file,
    get_menu_from_file,
    print_menu,
    print_contacts,
    parse_input,
    rewrite_contacts,
    show_contact,
    add_contact,
    change_contact,
    del_contact,
    birthdays,
    show_birthday,
    add_birthday,
)


# ----------------------------------------------------
# Головна програма
def main():
    """Головна програма-марштрутизатор"""
    data_dir = Path("data")
    data_file = Path("addressbook.pkl")
    data_path = data_dir / data_file
    contacts = get_data_from_file(data_path)

    changes = False
    menu_file = "cli_menu.csv"
    menu_path = data_dir / menu_file
    menu = get_menu_from_file(menu_path)

    print_tytle("Консольний бот-помічник")
    # Основний цикл програми
    while True:
        print_menu(menu)
        user_input = input("Введіть команду: ")
        command, *args = parse_input(user_input)
        if command == "hello":
            print("Чим я можу допомогти?\n")
        elif command == "all":
            print_contacts(contacts)
            input("Press Enter to continue...")
        elif command == "show":
            print(show_contact(args, contacts))
            input("Press Enter to continue...")
        elif command == "add":
            print(add_contact(args, contacts))
            changes = True
            input("Press Enter to continue...")
        elif command == "change":
            print(change_contact(args, contacts))
            changes = True
            input("Press Enter to continue...")
        elif command == "del" and args:
            print(del_contact(args, contacts))
            changes = True
            input("Press Enter to continue...")
        elif command == "show-birthday" and args:
            print(show_birthday(args, contacts))
            input("Press Enter to continue...")
        elif command == "birthdays":
            print(birthdays(contacts))
            input("Press Enter to continue...")
        elif command == "add-birthday" and args:
            print(add_birthday(args, contacts))
            changes = True
            input("Press Enter to continue...")
        elif command in ["close", "exit"]:
            if changes:
                answer = input("Дані змінено. Зберегти зміни ? y/n ")
                if answer.lower() == "y":
                    rewrite_contacts(contacts, data_path)
            print_end("До побачення!")
            break
        else:
            print("Невірна команда\n")


# ----------------------------------------------------
# Точка входу
if __name__ == "__main__":
    main()
else:
    log_error("Помилка виконання скрипта!")
