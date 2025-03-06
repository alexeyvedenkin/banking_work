from datetime import datetime
from unittest.mock import Mock, patch
from typing import Any
import unittest

import pytest

from src.utils import (get_start_for_period, get_start_of_month, get_start_of_week, get_start_of_year,
                       get_start_without_period, greeting, request_currency, stock_indices)


# def test_days_translation() -> None:
#     assert days_translation == test_days_translation


def test_get_start_of_week(test_date) -> None:
    expected = datetime(2021, 3, 29, 0, 0, 0)
    assert get_start_of_week(test_date) == expected


def test_get_start_of_week_type_error(test_date) -> None:
    with pytest.raises(TypeError):
        get_start_of_week(datetime('2011-11-11'))


def test_get_start_of_month(test_date):
    expected = datetime(2021, 3, 1, 0, 0, 0)
    assert get_start_of_month(test_date) == expected


def test_get_start_of_year(test_date) -> None:
    expected = datetime(2021, 1, 1, 0, 0, 0)
    assert get_start_of_year(test_date) == expected


def test_get_start_without_period(test_date) -> None:
    expected = datetime(1971, 1, 1, 0, 0, 0)
    assert get_start_without_period(test_date) == expected


def test_get_start_for_period(test_date_str, type_of_period='M') -> None:
    test_date = datetime.strptime(test_date_str, "%d.%m.%Y %H:%M:%S")
    if type_of_period == 'M':
        expected = datetime(2021, 3, 1, 0, 0, 0)
        assert get_start_for_period(test_date_str, 'M') == expected
    elif type_of_period == 'W':
        expected = datetime(2021, 3, 29, 0, 0, 0)
        assert get_start_for_period(test_date_str, 'W') == expected
    elif type_of_period == 'Y':
        expected = datetime(2021, 1, 1, 0, 0, 0)
        assert get_start_for_period(test_date_str, 'Y') == expected
    elif type_of_period == 'ALL':
        expected = datetime(1971, 1, 1, 0, 0, 0)
        assert get_start_for_period(test_date_str, 'ALL') == expected


@patch('datetime.datetime')
def test_greeting(datetime_mocked) -> None:
    datetime_mocked.now.return_value.hour = 13
    assert greeting() == 'Добрый день, уважаемый пользователь!'


@patch('requests.get')
def test_request_currency(mock_get: Any) -> None:
    # mock_get.currency_list[0].return_value = ["USD"]
    mock_response = unittest.mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"base_code": "USD", "conversion_rate": 100.05}
    mock_get.return_value = mock_response
    expected = [{"currency": "USD", "rate": 100.05}, {"currency": "EUR", "rate": 100.05}]
    assert request_currency('example.json') == expected


@patch('requests.get')
def test_stock_indices(mock_get: Any) -> None:
    # mock_get.currency_list[0].return_value = ["USD"]
    mock_response = unittest.mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"symbol": "AAPL", "close": 247.04}
    mock_get.return_value = mock_response
    expected = [{"stock": "AAPL", "price": 247.04}]
    assert stock_indices('test_stocks_json') == expected
