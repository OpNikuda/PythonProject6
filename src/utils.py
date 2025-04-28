import os
import json
import logging

# Настройка логгера
logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

log_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'utils.log')

file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)

# Логгирование ошибок через logging
def get_json(filename) -> list[dict]:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.exception(f"Файл не найден: {filename}")
    except json.JSONDecodeError:
        logger.exception(f"Ошибка декодирования JSON в файле: {filename}")
    except PermissionError:
        logger.exception(f"Нет доступа к файлу: {filename}")
    return []

