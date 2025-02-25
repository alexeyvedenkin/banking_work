from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from src.utils import (days_translation, greeting, get_start_for_period, get_start_of_month, get_start_of_week,
                       get_start_of_year, get_start_without_period)

# with patch(datetime.strptime('2021-03-31 23:59:59')) as mock_work_date:
#     mock_work_date.return_value = datetime.datetime(2021, 12, 27, 23, 59, 59)
#
# print(mock_work_date.return_value, type(mock_work_date.return_value))


# def test_get_work_datetime() -> None:
#     assert


def test_days_translation() -> None:
    assert days_translation == test_days_translation


def test_get_start_of_week(test_date) -> None:
    expected = datetime(2021, 3, 29, 0, 0, 0)
    assert get_start_of_week(test_date) == expected
    # assert get_start_of_week(mock_work_date.year) == 2021
    # assert get_start_of_week(mock_work_date.month) == 12
    # assert get_start_of_week(mock_work_date.day) == 27
    # assert get_start_of_week(mock_work_date.hour) == 0
    # assert get_start_of_week(mock_work_date.minute) == 0
    # assert get_start_of_week(mock_work_date.second) == 0


def test_get_start_of_week_type_error() -> None:
    with pytest.raises(TypeError):
        get_start_of_week(datetime.datetime('%ab %cd %ef %gh %hg %fe'))


# def test_get_start_of_month() -> None:
#     assert get_start_of_month(mock_work_date) == (2021, 12, 27, 23, 59, 59)
#     # assert get_start_of_month(mock_work_date.month) == 12
#     # assert get_start_of_month(mock_work_date.day) == 1
#     # assert get_start_of_month(mock_work_date.hour) == 0
#     # assert get_start_of_month(mock_work_date.minute) == 0
#     # assert get_start_of_month(mock_work_date.second) == 0
def test_get_start_of_month(test_date):
    # Arrange
    # work_date = datetime.datetime(2022, 9, 15, 10, 30, 0)
    expected = datetime(2021, 3, 0, 0, 0, 0)
    # start_of_month = get_start_of_month(work_date)
    # print(start_of_month, get_start_of_month(work_date))
    assert get_start_of_month(test_date) == expected

def test_get_start_of_year(test_date) -> None:
    expected = datetime(2021, 1, 0, 0, 0, 0)
    assert get_start_of_year(test_date) == expected
    # assert get_start_of_year(mock_work_date.month) == 1
    # assert get_start_of_year(mock_work_date.day) == 1
    # assert get_start_of_year(mock_work_date.hour) == 0
    # assert get_start_of_year(mock_work_date.minute) == 0
    # assert get_start_of_year(mock_work_date.second) == 0


def test_get_start_without_period(test_date) -> None:
    expected = datetime(1, 1, 0, 0, 0, 0)
    assert get_start_without_period(test_date) == expected
    # assert get_start_without_period(mock_work_date.month) == 1
    # assert get_start_without_period(mock_work_date.day) == 31
    # assert get_start_without_period(mock_work_date.hour) == 0
    # assert get_start_without_period(mock_work_date.minute) == 0
    # assert get_start_without_period(mock_work_date.second) == 0


# def test_get_start_for_period() -> None:
    # assert get_start_for_period(mock_work_date, 'W') == (2021, 12, 27, 0, 0, 0)
    # assert get_start_for_period(mock_work_date, 'M') == (2021, 12, 1, 0, 0, 0)
    # assert get_start_for_period(mock_work_date, 'Y') == (2021, 1, 1, 0, 0, 0)
    # assert get_start_for_period(mock_work_date, 'ALL') == (1, 1, 1, 0, 0, 0)


@patch('datetime.datetime')
def test_greeting(datetime_mocked) -> None:
    datetime_mocked.now.return_value.hour = 13
    assert greeting() == 'Добрый день, уважаемый пользователь!'
