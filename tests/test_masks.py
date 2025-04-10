from src.masks import get_mask_card_number, get_mask_account  # Предполагается, что код в src/masks.py
import pytest

def test_get_mask_card_number_valid():
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert get_mask_card_number(1234567890123456) == "1234 56** **** 3456"  # Проверка int
    assert get_mask_card_number("1234 5678 9012 3456") == "1234 56** **** 3456"  # С пробелами в номере


def test_get_mask_card_number_invalid():
    assert get_mask_card_number("123") == ""  # Слишком короткий номер
    assert get_mask_card_number("abcdefghij") == ""  # Не цифры
    assert get_mask_card_number("123456789") == ""  # Меньше 10 цифр
    assert get_mask_card_number("1234567890123456a") == "" # Содержит нецифровые символы


def test_get_mask_account_valid():
    assert get_mask_account("1234567890") == "******7890"
    assert get_mask_account(1234567890) == "******7890"  # Проверка int
    assert get_mask_account("1234 567890") == "******7890"  # С пробелами в номере
    assert get_mask_account("1234") == "1234" # проверка граничного случая (ровно 4 цифры)


def test_get_mask_account_invalid():
    assert get_mask_account("123") == ""  # Слишком короткий номер
    assert get_mask_account("abcd") == "" # Не цифры
    assert get_mask_account("abc1") == "" # Содержит нецифровые символы
    assert get_mask_account("") == "" # пустая строка
    assert get_mask_account(None) == "" # None в качестве аргумента
