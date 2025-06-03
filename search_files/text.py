def start_text() -> str:
    return '''Программа: Привет! Добро пожаловать в программу работы
с банковскими транзакциями. Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
4. Выход'''


def status_prompt_text() -> str:
    return '''Программа: Введите статус, по которому необходимо выполнить фильтрацию.
Доступные: EXECUTED, CANCELED, PENDING'''


def invalid_status_text(status: str) -> str:
    return f'Программа: Статус операции "{status}" недоступен.'


def sort_prompt_text() -> str:
    return "Программа: Отсортировать операции по дате?"


def sort_direction_prompt_text() -> str:
    return "Программа: Отсортировать по возрастанию или по убыванию?"


def currency_filter_prompt_text() -> str:
    return "Программа: Выводить только рублевые транзакции?"


def description_filter_prompt_text() -> str:
    return "Программа: Отфильтровать список транзакций по определенному слову в описании?"


def word_input_prompt_text() -> str:
    return "Программа: Введите слово для поиска в описании:"


def printing_transactions_text() -> str:
    return "Программа: Распечатываю итоговый список транзакций..."


def no_transactions_text() -> str:
    return "Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"


def transactions_count_text(count: int) -> str:
    if count % 10 == 1 and count % 100 != 11:
        word = "операция"
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        word = "операции"
    else:
        word = "операций"
    return f"Программа: Всего банковских {word} в выборке: {count}"


def transaction_separator() -> str:
    return "-" * 50