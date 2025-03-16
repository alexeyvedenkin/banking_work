import logging
import os
from functools import wraps

import pandas as pd

from config import LOGS_DIR, RESULT_DIR
from typing import Any

logger = logging.getLogger("decorator")
logger.setLevel(logging.DEBUG)
log_file_path = os.path.join(LOGS_DIR, 'decorator.log')
file_handler = logging.FileHandler(log_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def to_json_file(filename:str = 'reports.json') -> Any:
    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.info('Результат работы функции записан в переменную result')
            result: pd.DataFrame = func(*args, **kwargs)

            logger.info('Начало преобразования объекта Series в словарь')

            logger.info('Начало выгрузки отчета')
            reports_path = os.path.join(RESULT_DIR, filename)
            result.to_json(path_or_buf=reports_path, indent=4, force_ascii=False)

            logger.info('Окончание выгрузки отчета')
            return result
        return wrapper
    return decorator
