import datetime
import logging
import os
from datetime import timedelta
from typing import Any, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from config import LOGS_DIR
from src.decorator import to_json_file
from src.utils import days_translation

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
log_file_path = os.path.join(LOGS_DIR, 'reports.log')
file_handler = logging.FileHandler(log_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


@to_json_file('my_report.json')
def spending_by_weekday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> Any:
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

    return spend_by_weekday
