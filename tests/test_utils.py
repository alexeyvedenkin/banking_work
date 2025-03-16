import json
import os
import unittest
from datetime import datetime
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from requests.exceptions import HTTPError

from config import DATA_DIR
from src.utils import days_translation, get_start_for_period, request_currency, stock_indices


def test_days_translation() -> None:
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


@pytest.mark.parametrize("work_date, type_of_period, expected_start", [
    ("15.02.2025 10:00:00", 'W', "10.02.2025 00:00:00"),
    ("15.02.2025 10:00:00", 'M', "01.02.2025 00:00:00"),
    ("15.02.2025 10:00:00", 'Y', "01.01.2025 00:00:00"),
    ("15.02.2025 10:00:00", 'ALL', "01.01.1971 00:00:00"),
])
def test_get_start_for_period(work_date: str, type_of_period: str, expected_start: str) -> None:
    start = get_start_for_period(work_date, type_of_period)
    expected_start_datetime = datetime.strptime(expected_start, "%d.%m.%Y %H:%M:%S")
    assert start == expected_start_datetime


def test_get_start_for_period_invalid_type_of_period() -> None:
    with pytest.raises(ValueError):
        get_start_for_period("15.09.2024 10:00:00", 'Некорректный тип периода')


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


def test_request_currency_file_not_found():
    # Убедитесь, что файла не существует
    filename = 'non_existent_file.txt'
    with pytest.raises(FileNotFoundError):
        # попытка открыть файл
        open(filename, 'r')


def test_request_currency_file_not_found_logging(caplog):
    request_currency('non_existent_file.json')
    assert "Не задан путь к исходным данным" in caplog.text


def test_request_currency_api_key_not_found() -> None:
    os.environ['APIKEY_EXCHANGERATE'] = ''
    result = request_currency()
    assert result == []


def test_request_currency_http_error():
    os.environ['APIKEY_EXCHANGERATE'] = 'test_api_key'
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPError('HTTP Error')
        mock_get.return_value = mock_response
        result = request_currency()
        assert result == []


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


def test_stock_indices_file_not_found() -> None:
    # Убедитесь, что файла не существует
    filename = 'non_existent_file.txt'
    with pytest.raises(FileNotFoundError):
        # попытка открыть файл
        open(filename, 'r')


def test_stock_indices_file_not_found_logging(caplog) -> None:
    stock_indices('non_existent_file.json')
    assert "Не задан путь к исходным данным" in caplog.text


def test_stock_indices_api_key_not_found() -> None:
    os.environ['APIKEY_TWELVEDATA_STOCK'] = ''
    result = stock_indices()
    assert result == []


def test_stock_indices_http_error():
    os.environ['APIKEY_TWELVEDATA_STOCK'] = 'test_api_key'
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPError('HTTP Error')
        mock_get.return_value = mock_response
        result = stock_indices()
        assert result == []
