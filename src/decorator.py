import datetime
import json
import logging
import os
from datetime import timedelta
from functools import wraps
from typing import Optional
from reports import spending_by_weekday

import pandas as pd
from dateutil.relativedelta import relativedelta

from config import DATA_DIR, LOGS_DIR, RESULT_DIR
from utils import days_translation

logger = logging.getLogger("decorator")
logger.setLevel(logging.DEBUG)
log_file_path = os.path.join(LOGS_DIR, 'decorator.log')
file_handler = logging.FileHandler(log_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


# def spending_by_category(transactions: pd.DataFrame,
#                          category: str,
#                          date: Optional[str] = None) -> pd.DataFrame:
#     """Возвращает траты по заданной категории за последние три месяца (от переданной даты)
#     """
#     pass

# def dumping_to_json(spending_by_weekday):
#     def wrapper(*args, **kwargs):
#         print('Подготовка к выгрузке отчета')
#         reports_path = os.path.join(RESULT_DIR, 'reports.json')
#         result = spending_by_weekday(*args, **kwargs)
#         print(result, type(result))
#         with open(reports_path, 'w', encoding='utf-8') as json_file:
#             json.dump(result, json_file, indent=4, ensure_ascii=False)
#         print('Отчет выгружен в файл results/reports.json')
#         return result
#     return wrapper


def to_json_file(filename):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info('Результат работы функции записан в переменную result')
            result = func(*args, **kwargs)

            # Преобразуем объект Series в словарь вручную
            logger.info('Начало преобразования объекта Series в словарь')
            series_dict = {index: round(value, 2) for index, value in result.items()}

            # Выгружаем словарь в JSON-файл
            logger.info('Начало выгрузки отчета')
            reports_path = os.path.join(RESULT_DIR, 'reports.json')
            with open(reports_path, 'w', encoding='utf-8') as f:
                json.dump(series_dict, f, indent=4, ensure_ascii=False)
            logger.info('Окончание выгрузки отчета')
            return result
        return wrapper
    return decorator

# Создаем функцию, которая возвращает объект Series
@to_json_file('series.json')
def create_series():
    logger.info('Формирование функции для обработки')
    operations_path = os.path.join(DATA_DIR, 'operations.xlsx')
    df = pd.read_excel(operations_path)
    result = spending_by_weekday(df, '31.03.2021 23:59:59')
    return result

# Вызываем функцию
if __name__ == '__main__':
    series = create_series()
    print(series)
