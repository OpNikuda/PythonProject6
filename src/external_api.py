import os
import requests
import json
from pathlib import Path


def load_api_key():
    """Загружает API ключ из файла .env в корне проекта"""
    env_path = Path(__file__).parent.parent / '.env'
    try:
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('API_KEY='):
                    return line.strip().split('=')[1]
    except FileNotFoundError:
        return None
    return os.environ.get('API_KEY')


API_KEY = load_api_key()
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_to_rub(amount: float, currency: str) -> float:
    """Конвертирует сумму из USD или EUR в рубли"""
    if not API_KEY:
        raise ValueError("API_KEY не загружен. Проверьте файл .env или переменные окружения")

    headers = {"apikey": API_KEY}
    params = {"base": currency, "symbols": "RUB"}

    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        rate = response.json()["rates"]["RUB"]
        return round(amount * rate, 2)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе курса валют: {e}")
        return amount  # Возвращаем исходную сумму при ошибке


def get_amount_in_rub(transaction: dict) -> float:
    """Возвращает сумму транзакции в рублях"""
    if not transaction or 'operationAmount' not in transaction:
        return 0.0

    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"].upper()

        if currency == "RUB":
            return amount
        elif currency in ("USD", "EUR"):
            return convert_to_rub(amount, currency)
        else:
            return amount  # Возвращаем как есть для других валют
    except (KeyError, ValueError) as e:
        print(f"Ошибка обработки транзакции: {e}")
        return 0.0


def load_transactions(filename: str) -> list:
    """Загружает список транзакций из JSON файла"""
    try:
        # Получаем абсолютный путь к файлу в папке data (на один уровень выше src)
        file_path = Path(__file__).parent.parent / 'data' / filename
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки файла {filename}: {e}")
        return []


if __name__ == "__main__":
    # Загружаем транзакции
    transactions = load_transactions('operations.json')

    if not transactions:
        print("Не удалось загрузить транзакции или файл пуст")
    else:
        # Обрабатываем только выполненные транзакции
        executed_transactions = [t for t in transactions if isinstance(t, dict) and t.get('state') == 'EXECUTED']

        print(f"Всего транзакций: {len(transactions)}, из них выполнено: {len(executed_transactions)}\n")

        # Выводим информацию по транзакциям
        for i, transaction in enumerate(executed_transactions[:5], 1):  # Первые 5 для примера
            amount_rub = get_amount_in_rub(transaction)
            print(f"{i}. Транзакция ID: {transaction.get('id')}")
            print(
                f"   Сумма: {transaction['operationAmount']['amount']} {transaction['operationAmount']['currency']['code']}")
            print(f"   В рублях: {amount_rub:.2f} RUB")
            print(f"   Описание: {transaction.get('description')}")
            print(f"   Дата: {transaction.get('date')}\n")