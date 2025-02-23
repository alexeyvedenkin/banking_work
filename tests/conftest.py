import pytest
import datetime
from datetime import datetime
from src import utils


@pytest.fixture
def test_date() -> str:
    """
    Тестовые данные для применения datetime
    """
    test_date = datetime.datetime.strptime('31.03.2021 23:59:59', "%d.%m.%Y %H:%M:%S")

    return test_date


# def test_datetime() -> datetime.datetime:
#     """
#     Тестовые данные для применения datetime
#     """
#     test_dat_time = 2025-12-18 22:54:00
#
#     return test_dat_time


test_days_translation= {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье'
    }
assert test_days_translation['Monday'] == 'Понедельник'
