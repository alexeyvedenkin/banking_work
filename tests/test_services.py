import logging
import pytest
from typing import Any
import os
from src.services import find_people_pass


def test_find_people_pass(test_transactions) -> None:
    # Mock the logger
    import logging
    logging.disable(logging.CRITICAL)

    # Call the function
    result = find_people_pass(test_transactions)

    # Check if the result is correct
    expected_result = [
        {'Категория': 'Переводы', 'Описание': 'Иванов И.'},
        {'Категория': 'Переводы', 'Описание': 'Петров П.'},
        ]
    assert result == expected_result

def test_find_people_pass_empty_transactions():
    # Mock the logger
    import logging
    logging.disable(logging.CRITICAL)

    # Call the function
    result = find_people_pass([])

    # Check if the result is correct
    assert len(result) == 0

def test_find_people_pass_no_persons():
    # Mock the logger
    import logging
    logging.disable(logging.CRITICAL)

    # Define test data
    test_transactions = [
        {'Категория': 'Переводы', 'Описание': 'Зарплата за март'},
        {'Категория': 'Зарплата', 'Описание': 'Зарплата за март'}
    ]

    # Call the function
    result = find_people_pass(test_transactions)

    # Check if the result is correct
    assert len(result) == 0
