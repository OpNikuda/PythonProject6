# decorators.py
import time
from datetime import datetime
from functools import wraps


def log(filepath):
    """Декоратор для логирования вызовов функций в файл или консоль.

    Args:
        filepath (str): Путь к файлу для логирования. Если None, логи выводятся в консоль.

    Returns:
        function: Декорированная функция с логированием.
    """

    def decorator(func):
        @wraps(func)  # Сохраняем метаданные оригинальной функции
        def wrapper(*args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            # Логируем начало выполнения
            start_msg = f"{timestamp} - {func_name} - args: {args}, kwargs: {kwargs}"

            try:
                # Выполняем функцию и замеряем время
                start_time = time.time()
                result = func(*args, **kwargs)
                exec_time = time.time() - start_time

                # Логируем успешное выполнение
                success_msg = (f"{timestamp} - {func_name} - returned: {result} "
                               f"[execution time: {exec_time:.4f}s]")
                log_message = f"{start_msg}\n{success_msg}\n"

                if filepath:
                    with open(filepath, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    print(log_message)

                return result

            except Exception as e:
                # Логируем ошибку
                error_msg = (f"{timestamp} - {func_name} - failed: "
                             f"{type(e).__name__}: {str(e)}")
                log_message = f"{start_msg}\n{error_msg}\n"

                if filepath:
                    with open(filepath, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    print(log_message)

                raise  # Пробрасываем ошибку дальше

        return wrapper

    return decorator

