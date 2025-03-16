import logging
import os
from typing import Any
from unittest.mock import patch

import pandas as pd
from pandas import DataFrame

from config import LOGS_DIR, RESULT_DIR
from src.decorator import to_json_file  # Импортируйте декоратор

logger = logging.getLogger("decorator")
logger.setLevel(logging.DEBUG)
log_file_path = os.path.join(LOGS_DIR, 'decorator.log')
file_handler = logging.FileHandler(log_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def test_to_json_file() -> None:
    # Создание тестовых данных
    df = pd.DataFrame({'column1': [1, 2], 'column2': [3, 4]})

    # Определение функции для декорирования
    @to_json_file('test_report.json')
    def test_func() -> DataFrame:
        return df

    # Вызов функции и проверка результата
    result = test_func()
    assert result.equals(df)

    # Проверка, что был создан файл отчета
    reports_path = os.path.join(RESULT_DIR, 'test_report.json')
    assert os.path.exists(reports_path)

    # Удаление файла отчета после теста
    os.remove(reports_path)


@patch('src.decorator.logging')
def test_to_json_file_logging(mock_logging: Any) -> None:
    # Подготовка тестовых данных
    df = pd.DataFrame({'column1': [1, 2], 'column2': [3, 4]})

    # Определение функции для декорирования
    @to_json_file('test_report.json')
    def test_func() -> Any:
        return df

    # Вызов функции и проверка результата
    result = test_func()
    assert result.equals(df)


@patch('src.decorator.pd.DataFrame.to_json')
def test_to_json_file_to_json(mock_to_json: Any) -> None:
    # Подготовка тестовых данных
    df = pd.DataFrame({'column1': [1, 2], 'column2': [3, 4]})

    # Определение функции для декорирования
    @to_json_file('test_report.json')
    def test_func() -> DataFrame:
        return df

    # Вызов функции и проверка результата
    result = test_func()
    assert result.equals(df)

    # Проверка, что был вызван метод to_json
    path_or_buf = os.path.join(RESULT_DIR, 'test_report.json')
    mock_to_json.assert_called_once_with(path_or_buf=path_or_buf, indent=4, force_ascii=False)
