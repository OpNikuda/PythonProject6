import json

def get_json(filename) -> list[dict]:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return []