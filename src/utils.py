import json

def get_json() -> list[dict]:
    filename = 'C:\\Users\\Администратор\\PycharmProjects\\PythonProject6\\data\\operations.json'
    try:
        with open(filename, 'r', encoding='utf8') as file:
            data = json.load(file)

            return data

    except (FileNotFoundError, json.JSONDecodeError, PermissionError):

        return []