import json
import os


def get_json() -> list[dict]:
    # Получаем путь к папке, где находится текущий скрипт
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Формируем путь к файлу относительно скрипта
    filename = os.path.join(script_dir, "data", "operations.json")

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return []