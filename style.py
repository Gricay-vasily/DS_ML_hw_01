'''Module for print text in color'''
from colorama import Fore

_N = 50
TITLE_SEPARATOR = '*'*_N
TITLE_SEPARATOR_COLOR = Fore.GREEN
TITLE_TEXT_COLOR = Fore.GREEN

END_SEPARATOR = '+' * _N
END_SEPARATOR_COLOR = Fore.BLUE
END_TEXT_COLOR = Fore.MAGENTA

SECTION_SEPARATOR ='-'*(_N)
SECTION_SEPARATOR_COLOR = Fore.WHITE
SECTION_TEXT_COLOR = Fore.GREEN

# Декоратори:
def title(f):
    '''Decorator for title print'''
    def inner(*args, **kwargs):
        print(f'{TITLE_SEPARATOR_COLOR}{TITLE_SEPARATOR}{Fore.RESET}')
        f(*args, **kwargs)
        print(f'{TITLE_SEPARATOR_COLOR}{TITLE_SEPARATOR}{Fore.RESET}')
    return inner

def section(f):
    '''Decorator for section print'''
    def inner(*args, **kwargs):
        print(f'{SECTION_SEPARATOR_COLOR}{SECTION_SEPARATOR}{Fore.RESET}')
        f(*args, **kwargs)
        print(f'{SECTION_SEPARATOR_COLOR}{SECTION_SEPARATOR}{Fore.RESET}')
    return inner

def end_tytle(f):
    '''Decorator for end_title print'''
    def inner(*args, **kwargs):
        print(f'{END_SEPARATOR_COLOR}{END_SEPARATOR}{Fore.RESET}')
        f(*args, **kwargs)
        print(f'{END_SEPARATOR_COLOR}{END_SEPARATOR}{Fore.RESET}')
    return inner

# Внутрішні функції виведення повідомлень

@title
def print_tytle(text):
    '''Print Title in Decorator'''
    print(f'{TITLE_TEXT_COLOR}{text:^{_N}}{Fore.RESET}')

@section
def print_section(text):
    '''Print Section in Decorator'''
    print(f'    {SECTION_TEXT_COLOR}{text}{Fore.RESET}')

@end_tytle
def print_end(text):
    '''Print End in Decorator'''
    print(f'{END_TEXT_COLOR}{text:^{_N}}{Fore.RESET}')


def log_info(message):
    '''Print log_INFO'''
    print(f'{Fore.BLUE} [INFO] {Fore.YELLOW} {message} {Fore.RESET}')

def log_error(message):
    '''Print log_ERROR'''
    print(f'{Fore.RED} [ERROR] {Fore.YELLOW} {message} {Fore.RESET}')

# Тести
if __name__ == '__main__':
    print_tytle('tytle')
    print_section('section')
    print_end('END_text')
    log_info('info_message')
    log_error('error_message')
