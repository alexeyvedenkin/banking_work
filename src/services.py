import datetime
import json
import logging

from typing import Any, Dict, List

from utils import read_excel


def profitably_cacheback(data_dict):
    """Определяет наиболее выгодные категории для повышенного кэшбека
    """
    pass


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Возвращает сумму, которую удалось бы отложить в «Инвесткопилку».
    """
    pass


def easy_search(data_dict):
    """Возвращает JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории
    """
    pass


def find_phone(data_dict):
    """Возвращает JSON-файл со всеми транзакциями, содержащими в описании мобильные номера
    """
    pass


def find_people_pass(data_dict):
    """Возвращает JSON-файл со всеми транзакциями, которые относятся к переводам физлицам
    """
    pass
