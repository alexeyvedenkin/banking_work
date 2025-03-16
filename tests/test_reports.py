import pandas as pd
import pytest
from src.reports import spending_by_weekday


def test_spending_by_weekday() -> None:
    # Создаем тестовый датафрейм
    data = {
        'Дата операции': ['01.01.2022 12:00:00', '02.01.2022 13:00:00', '03.01.2022 14:00:00'],
        'Сумма операции': [-100, -200, -300]
    }
    transactions = pd.DataFrame(data)

    # Вызов функции
    result = spending_by_weekday(transactions, '01.04.2022 12:00:00')

    # Проверка результата
    assert isinstance(result, pd.Series)
    assert len(result) == 7  # 7 дней недели


def test_spending_by_weekday_empty() -> None:
    # Создаем пустой датафрейм
    transactions = pd.DataFrame({
        'Дата операции': [],
        'Сумма операции': []
    })

    # Вызов функции
    result = spending_by_weekday(transactions, '01.04.2022 12:00:00')

    # Проверка результата
    assert isinstance(result, pd.Series)
    assert len(result) == 7  # 7 дней недели

def test_spending_by_weekday_invalid_date() -> None:
    # Создаем тестовый датафрейм
    data = {
        'Дата операции': ['01.01.2022 12:00:00', '02.01.2022 13:00:00', '03.01.2022 14:00:00'],
        'Сумма операции': [-100, -200, -300]
    }
    transactions = pd.DataFrame(data)

    # Вызов функции с некорректной датой
    with pytest.raises(ValueError):
        spending_by_weekday(transactions, '01.04.2022')
