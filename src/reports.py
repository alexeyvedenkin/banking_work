import datetime
import json
import logging
import pandas as pd

from typing import Any, Dict, List, Optional

from utils import read_excel


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца (от переданной даты)
    """
    pass


def spending_by_weekday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты)
    """
    pass


def spending_by_workday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> pd.DataFrame:
    """Выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты)
    """
    pass
