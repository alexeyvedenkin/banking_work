import datetime
import logging
import os
from datetime import timedelta
from typing import Optional
import json

import pandas as pd
from dateutil.relativedelta import relativedelta

from config import LOGS_DIR, DATA_DIR, RESULT_DIR
from utils import days_translation

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
log_file_path = os.path.join(LOGS_DIR, 'reports.log')
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
#
# @dumping_to_json
def spending_by_weekday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты)
    """

    # Определяем период для обработки исходя из заданной даты
    work_date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    logger.info("Определенa исходная дата")
    start_of_period = work_date - relativedelta(months=3) + timedelta(seconds=1)
    logger.info("Определенa дата начала периода")
    print(f'Период выборки: с {start_of_period} до {work_date}')
    print()

    # Добавляем в датафрейм столбец с объектами datetime дла получения соответствующих дней недели
    transactions['date_from_datetime'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True)

    # Добавляем столбец с днями недели
    transactions['День недели'] = transactions['date_from_datetime'].dt.day_name().map(days_translation())

    # Устанавливаем индекс в соответствии с днями недели
    transactions['День недели'] = pd.Categorical(transactions['День недели'], categories=[
        'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота',
        'Воскресенье'
    ], ordered=True)

    # Фильтруем исходный датафрейм по заданному периоду и отрицательной сумме операции (платежи)
    filtered_transactions = transactions[(start_of_period <= transactions['date_from_datetime'])
                                         & (transactions['date_from_datetime'] <= work_date)
                                         & (transactions['Сумма операции'] < 0)
                                         ]

    # Сортируем по дням недели
    result = filtered_transactions.sort_values(by='День недели')
    # print(result)

    # Группируем по дням недели
    pays_by_weekday = result.groupby('День недели', observed=False)

    # Определяем сумму расходов по дням недели в заданном периоде
    spend_by_weekday = pays_by_weekday['Сумма операции'].apply(lambda x: x[x < 0].abs().sum())
    # spend_by_weekday_dict = spend_by_weekday.to_dict

    return spend_by_weekday


# def spending_by_workday(transactions: pd.DataFrame,
#                         date: Optional[str] = None) -> pd.DataFrame:
#     """Выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты)
#     """
#     pass


if __name__ == '__main__':
    operations_path = os.path.join(DATA_DIR, 'operations.xlsx')
    df = pd.read_excel(operations_path)
    print(spending_by_weekday(df, '31.03.2021 23:59:59'))
