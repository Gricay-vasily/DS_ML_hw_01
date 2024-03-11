"""Модуль Менеджер обробки файлів"""

from style import log_info


class FileManager:
    """Менеджер обробки файлів"""

    def __init__(self, path, mode="r", encoding="utf-8"):
        self.file = None
        self.opened = False
        self.path = path
        self.mode = mode
        self.encoding = encoding

    def __enter__(self):
        self.file = open(self.path, self.mode, encoding=self.encoding)
        self.opened = True
        log_info(f"Відкривається файл {self.path}")
        return self.file

    def __exit__(self, *args):
        log_info("Робота з даними через  with - завершена")
        if self.opened:
            log_info(f"Закривається файл {self.path}")
            log_info(f"Аргументи закриття файлу - {args}")
            self.file.close()
        self.opened = False


# Тести
if __name__ == "__main__":
    PATH = "data/cli_menu.cvs"
    menu = {}
    with FileManager(PATH) as fh:
        lines = fh.readlines()
    for line in lines:
        cmd, action = line.strip().split(
            ",", 1
        )  # Розбиття на елементи за заданим розділювачем
        menu[cmd] = action
    for k, v in menu.items():
        print(f"{k:<35}{v:<25}")
    print()
