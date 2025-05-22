from unittest.mock import patch, MagicMock, mock_open
from src.external_api import load_api_key, get_amount_in_rub


def test_load_api_key_from_file():
    """Тест загрузки API ключа из файла"""
    # Мокаем open, чтобы он читал строку с API_KEY
    with patch("builtins.open", mock_open(read_data="API_KEY=test123")), \
            patch("os.path.dirname", return_value="/fake/path"):
        # Проверяем, что функция возвращает правильный API ключ
        assert load_api_key() == "test123"


def test_get_amount_in_rub_with_patch():
    """
    Тестируем конвертацию валюты с мокингом API-запроса
    """
    # 1. Мокаем API-ответ (имитация запроса к внешнему сервису)
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"RUB": 90.5}}
    mock_response.raise_for_status.return_value = None

    # 2. Мокаем все зависимости (запросы, API_KEY)
    with patch("src.external_api.requests.get", return_value=mock_response), \
            patch("src.external_api.API_KEY", "test_key"):
        # Тест для EUR (100.0 EUR, должно быть 9050 RUB)
        eur_transaction = {"amount": "100.0", "currency": "EUR"}
        assert get_amount_in_rub(eur_transaction) == 9050.0

        # Тест для USD (100.0 USD, ожидаем результат по курсу)
        usd_transaction = {"amount": "100.0", "currency": "USD"}
        assert get_amount_in_rub(usd_transaction) == 9050.0  # Этот курс также нужно будет настроить в ответе mock_response

