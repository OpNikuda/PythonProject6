import pytest

@pytest.fixture
def valid_card_number():
    """Фикстура, возвращающая валидный номер карты."""
    return "1234567890123456"

@pytest.fixture
def short_card_number():
    """Фикстура, возвращающая короткий номер карты."""
    return "1234"

@pytest.fixture
def valid_account_number():
    """Фикстура, возвращающая валидный номер счета."""
    return "12345678901234567890"

@pytest.fixture
def short_account_number():
    """Фикстура, возвращающая короткий номер счета."""
    return "12345678"

@pytest.fixture
def invalid_input():
    """Фикстура, возвращающая невалидные входные данные (содержащие нецифровые символы)."""
    return "abc1234"

@pytest.fixture
def empty_input():
    """Фикстура, возвращающая пустую строку."""
    return ""