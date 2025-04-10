from src.proccesing import filter_by_state, sort_by_date  # Убедитесь, что путь верный
import pytest

def test_filter_by_state_executed():
    data = [
        {'state': 'EXECUTED', 'amount': 100},
        {'state': 'CANCELED', 'amount': 50},
        {'state': 'EXECUTED', 'amount': 200}
    ]
    expected = [
        {'state': 'EXECUTED', 'amount': 100},
        {'state': 'EXECUTED', 'amount': 200}
    ]
    assert filter_by_state(data) == expected
    assert filter_by_state(data, 'EXECUTED') == expected  # Явное указание состояния


def test_filter_by_state_canceled():
    data = [
        {'state': 'EXECUTED', 'amount': 100},
        {'state': 'CANCELED', 'amount': 50},
        {'state': 'EXECUTED', 'amount': 200}
    ]
    expected = [{'state': 'CANCELED', 'amount': 50}]
    assert filter_by_state(data, 'CANCELED') == expected


def test_filter_by_state_empty_list():
    assert filter_by_state([]) == []


def test_filter_by_state_no_matching_state():
    data = [
        {'state': 'EXECUTED', 'amount': 100},
        {'state': 'CANCELED', 'amount': 50}
    ]
    assert filter_by_state(data, 'PENDING') == []


def test_sort_by_date_empty_list():
    assert sort_by_date([]) == []
