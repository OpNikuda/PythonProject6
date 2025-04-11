# test_decorators.py
import os
import pytest
from datetime import datetime
from src.decorators import log


@pytest.fixture
def log_file(tmp_path):
    filepath = tmp_path / "test.log"
    yield str(filepath)
    if os.path.exists(filepath):
        os.remove(filepath)


def read_log_file(filepath):
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def test_log_success_to_file(log_file):
    """Проверка логирования успешного выполнения в файл"""

    @log(log_file)
    def add(a, b):
        return a + b

    result = add(2, 3)
    log_content = read_log_file(log_file)

    assert result == 5
    assert "add - args: (2, 3), kwargs: {}" in log_content
    assert "add - returned: 5" in log_content
    assert "failed" not in log_content


def test_log_error_to_file(log_file):
    """Проверка логирования ошибки в файл"""

    @log(log_file)
    def div(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(1, 0)

    log_content = read_log_file(log_file)
    assert "div - args: (1, 0), kwargs: {}" in log_content
    assert "ZeroDivisionError" in log_content
    assert "division by zero" in log_content


def test_log_to_console(capsys):
    """Проверка логирования в консоль при filepath=None"""

    @log(None)
    def mul(a, b):
        return a * b

    result = mul(3, 4)
    captured = capsys.readouterr()

    assert result == 12
    assert "mul - args: (3, 4), kwargs: {}" in captured.out
    assert "mul - returned: 12" in captured.out


def test_log_preserves_function_metadata(log_file):
    """Проверка сохранения метаданных функции"""

    @log(log_file)
    def example_func(a: int, b: int = 1) -> int:
        """Example function"""
        return a + b

    assert example_func.__name__ == "example_func"
    assert example_func.__doc__ == "Example function"
    assert example_func.__annotations__ == {"a": int, "b": int, "return": int}

##