import pytest
from datetime import datetime
from src import utils


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
def test_days_translation():
    return {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье'
    }
