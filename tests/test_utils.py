from datetime import datetime
from unittest.mock import Mock, patch
from typing import Any
import unittest
import os
import json

import pytest

from config import DATA_DIR
from src.utils import (days_translation, get_start_for_period, request_currency, stock_indices)


def test_days_translation():
    # Вызов функции
    days_dict = days_translation()

    # Проверка, что в словаре правильное количество элементов
    assert len(days_dict) == 7, "Неверное количество дней недели"

    # Проверка, что все необходимые дни недели присутствуют в словаре
    expected_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in expected_days:
        assert day in days_dict, f"Отсутствует день недели: {day}"

    # Проверка, что все значения в словаре не пусты
    for value in days_dict.values():
        assert value, "Найдено пустое значение в словаре"


# def test_get_start_of_week(test_date) -> None:
#     expected = datetime(2021, 3, 29, 0, 0, 0)
#     assert get_start_of_week(test_date) == expected
#
#
# def test_get_start_of_week_type_error(test_date) -> None:
#     with pytest.raises(TypeError):
#         get_start_of_week(datetime('2011-11-11'))
#
#
# def test_get_start_of_month(test_date):
#     expected = datetime(2021, 3, 1, 0, 0, 0)
#     assert get_start_of_month(test_date) == expected
#
#
# def test_get_start_of_year(test_date) -> None:
#     expected = datetime(2021, 1, 1, 0, 0, 0)
#     assert get_start_of_year(test_date) == expected
#
#
# def test_get_start_without_period(test_date) -> None:
#     test_date = datetime(1971,1,1)
#     expected = datetime(1971, 1, 1)
#     assert get_start_without_period(test_date) == expected


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


# @patch('datetime.datetime')
# def test_greeting(datetime_mocked) -> None:
#     datetime_mocked.now.return_value.hour = 13
#     assert greeting() == 'Добрый день, уважаемый пользователь!'


@patch('requests.get')
def test_request_currency(mock_get: Any) -> None:
    # Создание тестовых данных
    test_data = {
        "user_currencies": ["USD"],
        "user_stocks": ["AAPL"]
    }
    # Создаем тестовый JSON-файл
    file_path = os.path.join(DATA_DIR, 'test_dict')
    with open(file_path, 'w') as f:
        json.dump(test_data, f)
    # Чтение данных из временного JSON-файла
    with open(file_path, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data == test_data, "Данные не совпадают"
    mock_get.currency_list[0].return_value = ["USD"]
    mock_response = unittest.mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"base_code": "USD", "conversion_rate": 100.05}
    mock_get.return_value = mock_response
    expected = [{"currency": "USD", "rate": 100.05}]
    assert request_currency(file_path) == expected
    # Удаление временного файла
    os.remove(file_path)


@patch('requests.get')
def test_stock_indices(mock_get: Any) -> None:
    # Создание тестовых данных
    test_data = {
        "user_currencies": ["USD"],
        "user_stocks": ["AAPL"]
    }
    # Создаем тестовый JSON-файл
    file_path = os.path.join(DATA_DIR, 'test_dict')
    with open(file_path, 'w') as f:
        json.dump(test_data, f)
    # Чтение данных из временного JSON-файла
    with open(file_path, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data == test_data, "Данные не совпадают"
    mock_get.stock_indices[0].return_value = ["AAPL"]
    mock_response = unittest.mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"symbol": "AAPL", "close": 247.04}
    mock_get.return_value = mock_response
    expected = [{"stock": "AAPL", "price": 247.04}]
    assert stock_indices(file_path) == expected
    # Удаление временного файла
    os.remove(file_path)
