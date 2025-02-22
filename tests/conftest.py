import pytest
import datetime
from datetime import datetime


@pytest.fixture
def test_date() -> str:
    """
    Тестовые данные для применения datetime
    """
    test_dat = '31.12.2021 23:59:59'

    return test_dat


# def test_datetime() -> datetime.datetime:
#     """
#     Тестовые данные для применения datetime
#     """
#     test_dat_time = 2025-12-18 22:54:00
#
#     return test_dat_time


def test_days_translation() -> dict:
    test_days_on_russian = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье'
    }
    return test_days_on_russian
