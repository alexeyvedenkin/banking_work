import pytest
from unittest.mock import patch, MagicMock

from config import RESULT_DIR
from src.decorator import to_json_file  # Импортируйте декоратор
import pandas as pd
import os


def test_to_json_file():
    # Подготовьте тестовые данные
    df = pd.DataFrame({'column1': [1, 2], 'column2': [3, 4]})

    # Создайте функцию, которую мы будем декорировать
    @to_json_file('test_report.json')
    def test_func():
        return df

    # Вызовите функцию и проверьте результат
    result = test_func()
    assert result.equals(df)

    # Проверьте, что был создан файл отчета
    reports_path = os.path.join(RESULT_DIR, 'test_report.json')
    assert os.path.exists(reports_path)

    # Удалите файл отчета после теста
    os.remove(reports_path)

# @patch('src.decorator.logging')
# def test_to_json_file_logging(mock_logging):
#     # Подготовьте тестовые данные
#     df = pd.DataFrame({'column1': [1, 2], 'column2': [3, 4]})
#
#     # Создайте функцию, которую мы будем декорировать
#     @to_json_file('test_report.json')
#     def test_func():
#         return df
#
#     # Вызовите функцию и проверьте результат
#     result = test_func()
#     assert result.equals(df)
#
#     # Проверьте, что были вызваны методы логирования
#     mock_logging.info.assert_any_call('Результат работы функции записан в переменную result')
#     mock_logging.info.assert_any_call('Начало преобразования объекта Series в словарь')
#     mock_logging.info.assert_any_call('Начало выгрузки отчета')
#     # mock_loading.info.assert_any_call('Окончание выгрузки отчета')


@patch('src.decorator.pd.DataFrame.to_json')
def test_to_json_file_to_json(mock_to_json):
    # Подготовьте тестовые данные
    df = pd.DataFrame({'column1': [1, 2], 'column2': [3, 4]})

    # Создайте функцию, которую мы будем декорировать
    @to_json_file('test_report.json')
    def test_func():
        return df

    # Вызовите функцию и проверьте результат
    result = test_func()
    assert result.equals(df)

    # Проверьте, что был вызван метод to_json
    mock_to_json.assert_called_once_with(path_or_buf='result_dir/test_report.json', indent=4, force_ascii=False)
