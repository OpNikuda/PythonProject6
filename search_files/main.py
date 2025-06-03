import os
import json
from master_func import (
    json_open,
    process_transactions,
    get_user_choice,
    filter_by_status
)
from text import start_text, status_prompt_text


def process_json_file() -> None:
    """Обрабатывает JSON-файл с транзакциями: загружает, фильтрует и выводит транзакции.

    Обрабатывает возможные ошибки при загрузке файла (FileNotFoundError, JSONDecodeError).
    Запрашивает у пользователя статус для фильтрации и выводит отфильтрованные транзакции.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_path = os.path.join(base_dir, "data", "operations.json")

    try:
        transactions = json_open(file_path)
        print("\nПрограмма: JSON-файл успешно загружен.")

        status = get_user_choice(status_prompt_text(), ['EXECUTED', 'CANCELED', 'PENDING'])
        filtered = filter_by_status(transactions, status)
        process_transactions(filtered)

    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути: {file_path}")
    except json.JSONDecodeError:
        print("Ошибка: Некорректный JSON-файл.")
    except Exception as e:
        print(f"Ошибка: {e}")


def main() -> None:
    """Основная функция программы, предоставляющая пользовательское меню.

    Выводит стартовое сообщение и обрабатывает выбор пользователя:
    - 1: Обработать JSON-файл с транзакциями
    - 4: Выйти из программы
    Другие варианты пока не реализованы.
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