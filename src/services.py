import json
import logging
import os
import re

from config import LOGS_DIR, DATA_DIR, RESULT_DIR
import pandas as pd

from typing import Any, Dict, List

from utils import read_excel

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
log_file_path = os.path.join(LOGS_DIR, 'services.log')
file_handler = logging.FileHandler(log_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# def profitably_cacheback(data_dict):
#     """Определяет наиболее выгодные категории для повышенного кэшбека
#     """
#     pass
#
#
# def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
#     """Возвращает сумму, которую удалось бы отложить в «Инвесткопилку».
#     """
#     pass
#
#
# def easy_search(data_dict):
#     """Возвращает JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории
#     """
#     pass
#
#
# def find_phone(df):
#     """Возвращает JSON-файл со всеми транзакциями, содержащими в описании мобильные номера
#     """
#     pass


def find_people_pass(transactions: list[dict]) -> list[dict]:
    """Возвращает JSON-файл со всеми транзакциями, которые относятся к переводам физлицам
    """
    pattern = re.compile(r'\w+\s\w\.')
    logger.info("Определен шаблон для поиска в описании операций")
    result_list = []
    logger.info("Начало обработки данных")
    for transaction in transactions:
        if transaction.get('Категория') == 'Переводы' and re.search(pattern, transaction.get('Описание')):
            logger.debug("Найден перевод")
            result_list.append(transaction)
    print(*result_list[:5], sep='\n')
    people_pass_path = os.path.join(RESULT_DIR, 'people_pass.json')
    with open(people_pass_path, 'w', encoding='utf-8') as json_file:
        json.dump(result_list, json_file, indent=4, ensure_ascii=False)

    return result_list


if __name__ == '__main__':
    operations_path = os.path.join(DATA_DIR, 'operations.xlsx')
    df = pd.read_excel(operations_path)
    transactions = df.to_dict(orient="records")
    result = find_people_pass(transactions)
    print(*result[:5], sep='\n')
    print(len(result))
    people_pass_path = os.path.join(RESULT_DIR, 'people_pass.json')
    with open(people_pass_path, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, indent=4, ensure_ascii=False)
