import json
import os
import pandas as pd
from datetime import datetime
from typing import Any


def test_test_date(test_date: datetime) -> None:
    """Проверка фикстуры test_date
    """
    # Проверка, что дата соответствует ожидаемому значению
    expected_date = datetime(2021, 3, 31, 23, 59, 59)
    assert test_date == expected_date


def test_test_date_str(test_date_str: str) -> None:
    # Проверяем, что фикстура возвращает заданное значение
    assert test_date_str == '31.03.2021 23:59:59'


def test_test_stocks_json(test_stocks_json: list) -> None:
    # Проверяем, что фикстура возвращает список
    assert isinstance(test_stocks_json, list)

    # Проверяем, что список содержит ожидаемое значение
    assert test_stocks_json == ["AAPL"]


def test_days_translation_fixture(test_days_translation: dict) -> None:
    # Проверка наличия всех дней недели
    expected_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    assert set(test_days_translation.keys()) == set(expected_days)

    # Проверка точности перевода
    expected_translations = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье'
    }
    assert test_days_translation == expected_translations


def test_test_json_file(test_json_file: Any) -> None:
    # Считываем данные из файла
    with open(test_json_file, 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)

    # Проверяем, что данные верны
    assert loaded_data == {'user_currencies': ['USD', 'EUR']}

    # Проверяем, что файл существует
    assert test_json_file.exists()


def test_df_fixture(df):
    # Проверка того, что фикстура возвращает DataFrame
    assert isinstance(df, pd.DataFrame)

    # Проверка содержимого DataFrame
    assert df.shape == (3, 2)  # 3 строки, 2 столбца
    assert df.columns.tolist() == ['transaction', 'date']
    assert df['transaction'].tolist() == [1, 2, 3]
    assert df['date'].tolist() == ['2022-01-01', '2022-01-02', '2022-01-03']


def test_user_settings_path(user_settings_path):
    # Проверка существования файла
    assert os.path.exists(user_settings_path)

    # Проверка содержимого файла
    with open(user_settings_path, 'r') as file:
        data = json.load(file)
        assert data['currency'] == 'USD'
        assert data['stock'] == 'NASDAQ'
