import pandas as pd

def read_transactions_csv(file_path):
    """Чтение транзакций из CSV-файла."""
    try:
        df = pd.read_csv(file_path)
        transactions = df.to_dict('records')  # Конвертация DataFrame в список словарей
        return transactions
    except Exception as n:
        print(f"Ошибка при чтении CSV-файла: {n}")
        return []

def read_transactions_excel(file_path):
    """Чтение транзакций из XLSX-файла."""
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        transactions = df.to_dict('records')  # Конвертация DataFrame в список словарей
        return transactions
    except Exception as n:
        print(f"Ошибка при чтении Excel-файла: {n}")
        return []

