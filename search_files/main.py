import os
import json
from master_func import (
    json_open,
    get_user_choice,
    filter_by_status,
    sort_transactions,
    filter_by_currency,
    filter_by_description,
    format_transaction
)
from text import (
    start_text,
    status_prompt_text,
    currency_filter_prompt_text,
    sort_prompt_text,
    sort_direction_prompt_text,
    description_filter_prompt_text,
    word_input_prompt_text,
    printing_transactions_text,
    no_transactions_text,
    transactions_count_text,
    transaction_separator,
)


def process_json_file() -> None:
    """
    Обрабатывает JSON-файл с транзакциями: загружает, фильтрует, сортирует и выводит.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "operations.json")

    try:
        transactions = json_open(file_path)
        print("\nПрограмма: JSON-файл успешно загружен.")

        # Выбор статуса
        status = get_user_choice(status_prompt_text(), ['EXECUTED', 'CANCELED', 'PENDING'])
        filtered = filter_by_status(transactions, status)

        if not filtered:
            print(no_transactions_text())
            return

        # Сортировка по дате
        if get_user_choice(sort_prompt_text() + " (Да/Нет)", ['ДА', 'НЕТ']) == 'ДА':
            direction = get_user_choice(sort_direction_prompt_text() + " (ВОЗРАСТАНИЕ/УБЫВАНИЕ)",
                                      ['ВОЗРАСТАНИЕ', 'УБЫВАНИЕ'])
            reverse = (direction == 'УБЫВАНИЕ')
            filtered = sort_transactions(filtered, reverse=reverse)

        # Фильтрация по валюте
        if get_user_choice(currency_filter_prompt_text() + " (Да/Нет)", ['ДА', 'НЕТ']) == 'ДА':
            filtered = filter_by_currency(filtered, 'RUB')

        # Фильтрация по описанию
        if get_user_choice(description_filter_prompt_text() + " (Да/Нет)", ['ДА', 'НЕТ']) == 'ДА':
            keyword = input(word_input_prompt_text() + " ").strip()
            filtered = filter_by_description(filtered, keyword)

        # Вывод транзакций
        if not filtered:
            print("\n" + no_transactions_text())
        else:
            print("\n" + printing_transactions_text())
            print(transactions_count_text(len(filtered)))
            print(transaction_separator())

            for i, transaction in enumerate(filtered, 1):
                print(f"{i}. {format_transaction(transaction)}")
                print(transaction_separator())

    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути: {file_path}")
    except json.JSONDecodeError:
        print("Ошибка: Некорректный JSON-файл.")
    except Exception as e:
        print(f"Ошибка: {e}")


def main() -> None:
    """
    Основная функция программы. Показывает меню и обрабатывает ввод пользователя.
    """
    print(start_text())
    while True:
        choice = input("\nВведите номер пункта меню: ").strip()
        if choice == '1':
            process_json_file()
        elif choice == '4':
            print("Программа: Выход из программы...")
            break
        else:
            print("Программа: Этот пункт пока не реализован. Выберите 1 или 4.")


if __name__ == "__main__":
    main()