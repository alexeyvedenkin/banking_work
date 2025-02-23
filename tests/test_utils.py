import datetime
from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from src.utils import (days_translation, get_start_for_period, get_start_of_month, get_start_of_week,
                       get_start_of_year, get_start_without_period, get_work_datetime)

with patch(str(get_work_datetime)) as mock_work_date:
    mock_work_date.return_value = datetime(2021, 12, 27, 23, 59, 59, 0)

print(mock_work_date.return_value, type(mock_work_date.return_value))


def test_days_translation() -> None:
    assert test_days_translation['Monday'] == 'Понедельник'


def test_get_start_of_week() -> None:
    assert get_start_of_week(mock_work_date) == (2021, 12, 28, 0, 0, 0)
    # assert get_start_of_week(mock_work_date.year) == 2021
    # assert get_start_of_week(mock_work_date.month) == 12
    # assert get_start_of_week(mock_work_date.day) == 27
    # assert get_start_of_week(mock_work_date.hour) == 0
    # assert get_start_of_week(mock_work_date.minute) == 0
    # assert get_start_of_week(mock_work_date.second) == 0


def test_get_start_of_week_type_error() -> None:
    with pytest.raises(TypeError):
        get_start_of_week(datetime.datetime('%ab %cd %ef %gh %hg %fe'))


def test_get_start_of_month() -> None:
    assert get_start_of_month(mock_work_date) == (2021, 12, 27, 23, 59, 59)
    # assert get_start_of_month(mock_work_date.month) == 12
    # assert get_start_of_month(mock_work_date.day) == 1
    # assert get_start_of_month(mock_work_date.hour) == 0
    # assert get_start_of_month(mock_work_date.minute) == 0
    # assert get_start_of_month(mock_work_date.second) == 0


def test_get_start_of_year() -> None:
    assert get_start_of_year(mock_work_date) == (2021, 1, 1, 0, 0, 0)
    # assert get_start_of_year(mock_work_date.month) == 1
    # assert get_start_of_year(mock_work_date.day) == 1
    # assert get_start_of_year(mock_work_date.hour) == 0
    # assert get_start_of_year(mock_work_date.minute) == 0
    # assert get_start_of_year(mock_work_date.second) == 0


def test_get_start_without_period() -> None:
    assert get_start_without_period(mock_work_date) == (1, 1, 1, 0, 0, 0)
    # assert get_start_without_period(mock_work_date.month) == 1
    # assert get_start_without_period(mock_work_date.day) == 31
    # assert get_start_without_period(mock_work_date.hour) == 0
    # assert get_start_without_period(mock_work_date.minute) == 0
    # assert get_start_without_period(mock_work_date.second) == 0


def test_get_start_for_period() -> None:
    assert get_start_for_period(mock_work_date, 'W') == (2021, 12, 27, 0, 0, 0)
    assert get_start_for_period(mock_work_date, 'M') == (2021, 12, 1, 0, 0, 0)
    assert get_start_for_period(mock_work_date, 'Y') == (2021, 1, 1, 0, 0, 0)
    assert get_start_for_period(mock_work_date, 'ALL') == (1, 1, 1, 0, 0, 0)
