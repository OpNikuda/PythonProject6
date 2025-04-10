
# 🏦 Банковские инструменты

Проект предоставляет набор инструментов для работы с банковскими данными, включая маскировку реквизитов и обработку транзакций.

## 📦 Установка

1. Клонируйте репозиторий:
```
git clone https://github.com/OpNikuda/PythonProject.git
```
Установите зависимости:
```
pip install -r requirements.txt
```
🔐 Модуль маскировки данных
Функции
```
mask_card_number(card_number: str) -> str
```

# Маскирует номер карты, оставляя последние 4 цифры.
## Пример:
```
mask_card_number("1234567890123456")  # "************3456"
mask_account_number(account_number: str) -> str
```

# Маскирует номер счета, оставляя первые и последние 4 цифры.
## Пример:
```
mask_account_number("12345678901234567890")  # "1234**********7890"
mask_account_card(payment_info: str) -> str
```

# Автоматически определяет тип реквизитов и применяет соответствующую маскировку.

## Пример:
```
mask_account_card("1234567890123456")  # "************3456"
mask_account_card("12345678901234567890")  # "1234**********7890"
```
# 🛠 Модуль generators
Функции
```
filter_by_currency(transactions: list, currency: str) -> Iterator[dict]
```

# Фильтрует транзакции по валюте.
## Пример:
```
for transaction in filter_by_currency(transactions, "USD"):
    print(transaction["id"])
transaction_descriptions(transactions: list) -> Iterator[str]
```

# Извлекает описания транзакций.
## Пример:
```
for desc in transaction_descriptions(transactions):
    print(desc)
card_number_generator(start: int, end: int) -> Iterator[str]
```

# Генерирует номера карт в заданном диапазоне.
## Пример:
```
for card in card_number_generator(1, 5):
    print(card)  # "0000 0000 0000 0001", ..., "0000 0000 0000 0005"
```

# 📊 Модуль обработки транзакций
Функции
```filter_by_state(data: list, state: str = 'EXECUTED') -> list
```

# Фильтрует список операций по состоянию.

## Параметры:

data - список операций

state - состояние для фильтрации (по умолчанию 'EXECUTED')

# Пример:
```
from src.processing import filter_by_state

transactions = [
    {'state': 'EXECUTED', 'amount': 100},
    {'state': 'CANCELED', 'amount': 50}
]

executed = filter_by_state(transactions)  # Только EXECUTED
sort_by_date(list_of_dicts: list, reverse: bool = True) -> list
```
# Сортирует операции по дате.

## Параметры:
```
list_of_dicts - список операций

reverse - сортировка по убыванию (True) или возрастанию (False)
```
## Пример:
```
from src.processing import sort_by_date

transactions = [
    {'date': '2023-01-01T12:00:00'},
    {'date': '2023-01-15T08:30:00'}
]

sorted_trans = sort_by_date(transactions)  # От новых к старым
```

# 🔐 Модуль маскировки данных
Функции
```
get_mask_card_number(card_number: str | int) -> str
```
Маскирует номер карты, оставляя первые 6 и последние 4 цифры.

## Параметры:

```
card_number - номер карты (может содержать пробелы)
```

Возвращает:

Замаскированный номер в формате "XXXX XX** **** XXXX"

Пустую строку для невалидных номеров

## Пример:
```
from src.masking_functions import get_mask_card_number
```
```
masked = get_mask_card_number("1234567890123456")  # "1234 56** **** 3456"
masked = get_mask_card_number(1234567890123456)    # "1234 56** **** 3456"
get_mask_account(account_number: str | int) -> str
```

Маскирует номер счета, оставляя последние 4 цифры.

## Параметры:

```
account_number - номер счета (может содержать пробелы)
```

Возвращает:

Замаскированный номер в формате "********XXXX"

Пустую строку для невалидных номеров

## Пример:
```
from src.masking_functions import get_mask_account
masked = get_mask_account("123456789012")  # "********9012"
masked = get_mask_account(123456789012)    # "********9012"
```

# 🧪 Тестирование
Запуск всех тестов:
```
pytest --cov=src --cov=generators --cov-report=term-missing
```

# Проверка стиля кода:
```
flake8 src/ generators/
```

# 📜 Лицензия
MIT © Nikonorov.M

