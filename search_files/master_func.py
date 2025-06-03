import json
import re
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict, Counter


def json_open(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает JSON-файл и возвращает список транзакций.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def filter_by_status(transactions: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданному статусу.
    """
    status_counter = Counter(t.get('state', '').upper() for t in transactions)
    print(f"Статистика по статусам: {dict(status_counter)}")
    return [t for t in transactions if t.get('state', '').upper() == status.upper()]


def filter_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по слову в описании.
    """
    pattern = re.compile(r'\b' + re.escape(search_string) + r'\b', re.IGNORECASE)
    return [t for t in transactions if 'description' in t and pattern.search(t['description'])]


def sort_transactions(transactions: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.
    """
    def get_date(transaction: Dict[str, Any]) -> datetime:
        date_str = transaction.get('date', '')
        try:
            if 'T' in date_str:
                return datetime.fromisoformat(date_str)
            return datetime.strptime(date_str, '%d.%m.%Y')
        except (ValueError, TypeError):
            return datetime.min

    return sorted(transactions, key=get_date, reverse=reverse)


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str = 'RUB') -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте (по умолчанию RUB).
    """
    currency = currency.upper()
    currency_stats = Counter(
        t.get('operationAmount', {}).get('currency', {}).get('code', '').upper()
        for t in transactions
    )
    print(f"Статистика по валютам: {dict(currency_stats)}")
    return [
        t for t in transactions
        if t.get('operationAmount', {}).get('currency', {}).get('code', '').upper() == currency
    ]


def mask_card_number(number: str) -> str:
    """
    Маскирует номер карты: первые 6, затем ** ****, и последние 4.
    """
    if not number:
        return ''
    if re.fullmatch(r'\d{16,19}', number):
        return f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
    return number


def get_user_choice(prompt: str, options: List[str]) -> str:
    """
    Запрашивает ввод у пользователя с валидацией по списку допустимых вариантов.
    """
    while True:
        print(prompt)
        choice = input("Ваш выбор: ").strip().upper()
        if choice in options:
            return choice
        print(f"Неверный ввод. Допустимые варианты: {', '.join(options)}")


def format_transaction(transaction: Dict[str, Any]) -> str:
    """
    Форматирует транзакцию для вывода.
    """
    parts = []

    if 'date' in transaction:
        date_str = transaction['date']
        match = re.match(r'(\d{4}-\d{2}-\d{2})T?', date_str)
        if match:
            formatted_date = datetime.strptime(match.group(1), '%Y-%m-%d').strftime('%d.%m.%Y')
            parts.append(formatted_date)

    if 'description' in transaction:
        parts.append(transaction['description'])

    if 'from' in transaction:
        sender = transaction['from']
        if re.search(r'счет', sender, re.IGNORECASE):
            acc = re.search(r'\d+', sender)
            if acc:
                parts.append(f"Счет **{acc.group()[-4:]}")
        else:
            chunks = sender.split()
            num = chunks[-1]
            masked = mask_card_number(num)
            parts.append(f"{' '.join(chunks[:-1])} {masked}")

    if 'to' in transaction:
        recipient = transaction['to']
        if re.search(r'счет', recipient, re.IGNORECASE):
            acc = re.search(r'\d+', recipient)
            if acc:
                parts.append(f"-> Счет **{acc.group()[-4:]}")
        else:
            chunks = recipient.split()
            num = chunks[-1]
            masked = mask_card_number(num)
            parts.append(f"-> {' '.join(chunks[:-1])} {masked}")

    if 'operationAmount' in transaction:
        amount = transaction['operationAmount']
        parts.append(f"{amount['amount']} {amount['currency']['code']}")

    return '\n'.join(parts)