from src.widget import mask_card_number, mask_account_number, mask_account_card
import pytest


def test_mask_account_card_valid_card():
    assert mask_account_card("1234567890123456") == "************3456"
    assert mask_account_card("1234") == "1234"



