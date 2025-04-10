import time
from datetime import datetime


def log(filepath):
    """Декоратор для логирования в файл"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Засекаем время
            start_time = time.time()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)
                exec_time = time.time() - start_time

                # Формируем запись лога
                log_entry = (
                    f"[{timestamp}] {func.__name__} - УСПЕХ\n"
                    f"Аргументы: args={args}, kwargs={kwargs}\n"
                    f"Результат: {result}\n"
                    f"Время выполнения: {exec_time:.4f} сек\n"
                    f"{'-' * 50}\n"
                )

                # Записываем в файл
                with open(filepath, "a", encoding="utf-8") as f:
                    f.write(log_entry)

                return result

            except Exception as e:
                # Логируем ошибку
                error_entry = (
                    f"[{timestamp}] {func.__name__} - ОШИБКА\n"
                    f"Аргументы: args={args}, kwargs={kwargs}\n"
                    f"Тип ошибки: {type(e).__name__}\n"
                    f"Сообщение: {str(e)}\n"
                    f"{'-' * 50}\n"
                )

                with open(filepath, "a", encoding="utf-8") as f:
                    f.write(error_entry)

                raise  # Пробрасываем ошибку дальше

        return wrapper

    return decorator


# Пример использования
@log("my_app.log")  # Все логи будут в файле my_app.log
def calculate(a, b):
    return a / b


# Тестируем (только при непосредственном запуске файла, а не при импорте)
if __name__ == "__main__":
    calculate(10, 2)  # Запишет успешный результат
    calculate(10, 0)  # Запишет ошибку деления на ноль

######