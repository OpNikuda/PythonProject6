from unittest.mock import mock_open, patch
import json
from src.utils import get_json

def test_get_json_success():
    """Тест успешного чтения JSON"""
    test_data = [{"id": 1, "name": "Test"}]
    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))), \
         patch("os.path.abspath"), \
         patch("os.path.dirname"), \
         patch("os.path.join"):
        assert get_json() == test_data

def test_get_json_file_not_found():
    """Тест отсутствия файла"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        assert get_json() == []