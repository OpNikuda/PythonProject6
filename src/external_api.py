import os
import requests


def load_api_key():
    """Загружает API ключ из файла .env в корне проекта"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
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
    headers = {"apikey": API_KEY}
    params = {"base": currency, "symbols": "RUB"}

    response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    rate = response.json()["rates"]["RUB"]
    return round(amount * rate, 2)


def get_amount_in_rub(transaction: dict) -> float:
    """Возвращает сумму транзакции в рублях"""
    amount = float(transaction["amount"])
    currency = transaction.get("currency", "RUB").upper()

    if currency == "RUB":
        return amount
    elif currency in ("USD", "EUR"):
        return convert_to_rub(amount, currency)
    return amount  # Возвращаем как есть, если валюта не распознана





# Пример транзакции в EUR
transaction_eur = {
    "amount": 50.0,  # Сумма в EUR
    "currency": "EUR"  # Валюта
}

# Получаем сумму в рублях
amount_in_rub = get_amount_in_rub(transaction_eur)
print(f"Сумма в рублях: {amount_in_rub} RUB")
