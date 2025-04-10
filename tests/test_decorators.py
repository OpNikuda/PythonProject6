import os
import pytest
from datetime import datetime
from src.decorators import log


def read_last_log_entry(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        return "".join(lines[-5:]) if lines else ""


# Фикстура для временного лог-файла
@pytest.fixture
def log_file(tmp_path):
    filepath = tmp_path / "test.log"
    yield str(filepath)  # Преобразуем Path в строку
    if os.path.exists(filepath):
        os.remove(filepath)


def test_log_success(log_file):
    """Проверка записи успешного выполнения"""

    @log(log_file)  # Применяем декоратор с текущим log_file
    def local_test_func(a, b=1):
        return a * b

    result = local_test_func(5, b=2)
    log_entry = read_last_log_entry(log_file)

    assert result == 10
    assert "local_test_func - УСПЕХ" in log_entry
    assert "Аргументы: args=(5,), kwargs={'b': 2}" in log_entry
    assert "Результат: 10" in log_entry
    assert "Время выполнения:" in log_entry


def test_log_error(log_file):
    """Проверка записи ошибки"""

    @log(log_file)
    def error_func():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        error_func()

    log_entry = read_last_log_entry(log_file)
    assert "error_func - ОШИБКА" in log_entry
    assert "Тип ошибки: ValueError" in log_entry
    assert "Сообщение: Test error" in log_entry


def test_log_format(log_file):
    """Проверка формата записи"""

    @log(log_file)  # Применяем декоратор с текущим log_file
    def local_test_func(a, b=1):
        return a * b

    local_test_func(3)
    log_entry = read_last_log_entry(log_file)

    # Проверяем временную метку
    timestamp = datetime.now().strftime("%Y-%m-%d %H:")
    assert timestamp in log_entry

    # Проверяем разделитель
    assert "-" * 50 in log_entry


def test_log_preserves_return_value(log_file):
    """Проверка, что декоратор не ломает возвращаемое значение"""

    @log(log_file)
    def sum_func(a, b):
        return a + b

    assert sum_func(2, 3) == 5

##