import datetime
import logging
from datetime import timedelta

import pandas as pd

from typing import Optional

from dateutil.relativedelta import relativedelta

from utils import days_translation

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs/reports.log', "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


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

    # Определяем период для обработки исходя из заданной даты
    work_date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    start_of_period = work_date - relativedelta(months=3) + timedelta(seconds=1)
    print(start_of_period, work_date)

    # Добавляем в датафрейм столбец с объектами datetime дла получения соответствующих дней недели
    transactions['date_from_datetime'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True)

    # Добавляем столбец с днями недели
    transactions['День недели'] = transactions['date_from_datetime'].dt.day_name().map(days_translation())

    # Устанавливаем индекс в соответствии с днями недели
    transactions['День недели'] = pd.Categorical(df['День недели'], categories=[
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
    pays_by_weekday = result.groupby('День недели')
    # print(pays_by_weekday)

    # Определяем сумму расходов по дням недели в заданном периоде
    spend_by_weekday = pays_by_weekday['Сумма операции'].apply(lambda x: x[x < 0].abs().sum())
    # print(spend_by_weekday)
    # result = result.sort_values(by='day_of_week')

    return spend_by_weekday


def spending_by_workday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> pd.DataFrame:
    """Выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты)
    """
    pass


if __name__ == '__main__':
    df = pd.read_excel('operations.xlsx')
    print(spending_by_weekday(df, '28.12.2021 16:15:14'))
