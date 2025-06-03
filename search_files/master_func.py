import json
import re
from datetime import datetime
from typing import List, Dict, Any, Union
from text import *


def json_open(file_path: str) -> List[Dict[str, Any]]:
    """Открывает и загружает JSON-файл.

    Args:
        file_path: Путь к JSON-файлу

    Returns:
        Список словарей с данными транзакций

    Raises:
        JSONDecodeError: Если файл содержит некорректный JSON
        IOError: При проблемах с чтением файла
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_user_choice(prompt: str, options: List[str]) -> str:
    """Запрашивает у пользователя выбор из заданных вариантов.

    Args:
        prompt: Текст приглашения для ввода
        options: Список допустимых вариантов выбора

    Returns:
        Выбранный пользователем вариант (в верхнем регистре)
    """
    while True:
        print(prompt)
        choice = input("Ваш выбор: ").strip().upper()
        if choice in options:
            return choice
        print(f"Неверный ввод. Допустимые варианты: {', '.join(options)}")


def get_yes_no_input(prompt: str) -> bool:
    """Запрашивает у пользователя ответ Да/Нет.

    Args:
        prompt: Текст вопроса

    Returns:
        True если ответ Да, False если ответ Нет
    """
    while True:
        answer = input(f"{prompt} (Да/Нет): ").strip().lower()
        if answer in ['да', 'д']:
            return True
        elif answer in ['нет', 'н']:
            return False
        print("Пожалуйста, введите 'Да' или 'Нет'")


def get_sort_direction() -> bool:
    """Запрашивает у пользователя направление сортировки.

    Returns:
        True для сортировки по убыванию, False по возрастанию
    """
    while True:
        answer = input(f"{sort_direction_prompt_text()} ").strip().lower()
        if answer in ['по возрастанию', 'возрастанию', 'возрастание']:
            return False
        elif answer in ['по убыванию', 'убыванию', 'убывание']:
            return True
        print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'")


def filter_by_status(transactions: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу.

    Args:
        transactions: Список транзакций
        status: Статус для фильтрации (EXECUTED, CANCELED, PENDING)

    Returns:
        Отфильтрованный список транзакций
    """
    return [t for t in transactions if t.get('state', '').upper() == status.upper()]


def sort_transactions(transactions: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате.

    Args:
        transactions: Список транзакций
        reverse: Направление сортировки (False - по возрастанию, True - по убыванию)

    Returns:
        Отсортированный список транзакций
    """

    def get_date(transaction):
        if 'date' not in transaction:
            return datetime.min
        try:
            return datetime.fromisoformat(transaction['date'])
        except ValueError:
            try:
                return datetime.strptime(transaction['date'], '%d.%m.%Y')
            except ValueError:
                return datetime.min

    return sorted(transactions, key=get_date, reverse=reverse)


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str = 'RUB') -> List[Dict[str, Any]]:
    """Фильтрует транзакции по валюте.

    Args:
        transactions: Список транзакций
        currency: Код валюты для фильтрации (по умолчанию RUB)

    Returns:
        Отфильтрованный список транзакций
    """
    return [t for t in transactions
            if t.get('operationAmount', {}).get('currency', {}).get('code', '').upper() == currency.upper()]


def filter_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по ключевому слову в описании.

    Args:
        transactions: Список транзакций
        search_string: Строка для поиска в описании

    Returns:
        Отфильтрованный список транзакций
    """
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [t for t in transactions if 'description' in t and pattern.search(t['description'])]


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию в читаемый вид.

    Args:
        transaction: Словарь с данными транзакции

    Returns:
        Отформатированная строка с данными транзакции
    """
    parts = []
    if 'date' in transaction:
        try:
            date = datetime.fromisoformat(transaction['date']).strftime('%d.%m.%Y')
        except ValueError:
            date = transaction['date']
        parts.append(date)

    if 'description' in transaction:
        parts.append(transaction['description'])

    if 'from' in transaction:
        from_ = transaction['from']
        if 'счет' in from_.lower():
            parts.append(f"Счет **{from_[-4:]}")
        else:
            card_parts = from_.split()
            number = card_parts[-1]
            masked = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
            parts.append(f"{' '.join(card_parts[:-1])} {masked}")

    if 'to' in transaction:
        to = transaction['to']
        if 'счет' in to.lower():
            parts.append(f"-> Счет **{to[-4:]}")
        else:
            card_parts = to.split()
            number = card_parts[-1]
            masked = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
            parts.append(f"-> {' '.join(card_parts[:-1])} {masked}")

    if 'operationAmount' in transaction:
        amount = transaction['operationAmount']
        parts.append(f"{amount['amount']} {amount['currency']['code']}")

    return '\n'.join(parts)


def process_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Обрабатывает список транзакций: сортирует, фильтрует и выводит результат.

    Args:
        transactions: Список транзакций для обработки
    """
    if not transactions:
        print(no_transactions_text())
        return

    if get_yes_no_input(sort_prompt_text()):
        reverse = get_sort_direction()
        transactions = sort_transactions(transactions, reverse)

    if get_yes_no_input(currency_filter_prompt_text()):
        transactions = filter_by_currency(transactions, 'RUB')

    if get_yes_no_input(description_filter_prompt_text()):
        print(word_input_prompt_text(), end=' ')
        search_word = input().strip()
        transactions = filter_by_description(transactions, search_word)

    if not transactions:
        print(no_transactions_text())
        return

    print(f"\n{printing_transactions_text()}\n")
    print(transactions_count_text(len(transactions)))

    for transaction in transactions:
        print(f"\n{format_transaction(transaction)}")
        print(transaction_separator())