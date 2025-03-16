import json
from datetime import datetime
from typing import Any

import pytest


@pytest.fixture
def test_date() -> datetime:
    """
    Тестовые данные для применения datetime
    """
    test_date = datetime.strptime('31.03.2021 23:59:59', "%d.%m.%Y %H:%M:%S")
    return test_date


@pytest.fixture
def test_date_str() -> str:
    """
    Тестовые данные для применения datetime
    """
    test_date_str = '31.03.2021 23:59:59'
    return test_date_str


@pytest.fixture
def test_stocks_json() -> list[str]:
    """
    Тестовые данные для применения stocks
    """
    test_stocks_json = ["AAPL"]
    return test_stocks_json


@pytest.fixture
def test_days_translation() -> dict:
    return {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье'
    }


# Тестовый JSON-файл
@pytest.fixture
def test_json_file(tmp_path: Any) -> Any:
    data = {'user_currencies': ['USD', 'EUR']}
    file_path = tmp_path / 'user_settings.json'
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file)
    return file_path


@pytest.fixture
def test_transactions() -> Any:
    return[
        {'Категория': 'Переводы', 'Описание': 'Иванов И.'},
        {'Категория': 'Зарплата', 'Описание': 'Зарплата за март'},
        {'Категория': 'Переводы', 'Описание': 'Петров П.'}
        ]
