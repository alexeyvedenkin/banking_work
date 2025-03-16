import json
import logging
import os
import re

from config import LOGS_DIR, RESULT_DIR

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
log_file_path = os.path.join(LOGS_DIR, 'services.log')
file_handler = logging.FileHandler(log_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


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
