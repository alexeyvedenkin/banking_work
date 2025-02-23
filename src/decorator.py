import datetime
import json
import logging
import os
from datetime import timedelta
from functools import wraps
from typing import Optional

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

def dumping_to_json(spending_by_weekday):
    def wrapper(*args, **kwargs):
        print('Подготовка к выгрузке отчета')
        reports_path = os.path.join(RESULT_DIR, 'reports.json')
        result = spending_by_weekday(*args, **kwargs)
        print(result, type(result))
        with open(reports_path, 'w', encoding='utf-8') as json_file:
            json.dump(result, json_file, indent=4, ensure_ascii=False)
        print('Отчет выгружен в файл results/reports.json')
        return result
    return wrapper