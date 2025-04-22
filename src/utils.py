import json
from importlib.resources import files


def get_json() -> list[dict]:
    try:
        # Используем importlib.resources для доступа к файлу в пакете
        data_package = files('data')
        with (data_package / 'operations.json').open('r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return []