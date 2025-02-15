import datetime
import json
import logging
import re

import pandas as pd

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


def find_phone(df):
    """Возвращает JSON-файл со всеми транзакциями, содержащими в описании мобильные номера
    """
    pass


def find_people_pass(df):
    """Возвращает JSON-файл со всеми транзакциями, которые относятся к переводам физлицам
    """
    filtered_data = df[df['Описание'].str.contains('Перевод')]
    result_list = filtered_data.sort_values(by='Дата операции', ascending=True)
    result_list.to_json('people_pass.json', indent=4, orient='records', force_ascii=False)
    return result_list


if __name__ == '__main__':
    df = pd.read_excel('operations.xlsx')
    result = find_people_pass(df)
    print(find_people_pass(df), sep='\n')
