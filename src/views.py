import datetime
# import json
# import logging
import pandas as pd
#
# from typing import Any, Dict, List, Optional
#
from pandas import DataFrame

from src import utils


def main_page():
    """Возвращает JSON-ответ по настройкам
    """
    pass


def events_page():
    """Возвращает JSON-ответ по настройкам
    """
    pass


def spending_by_period(df, work_date: str, type_of_period: str='W') -> DataFrame:
    """Возвращает общую сумму расходов за период
    """
    # Определяем период для обработки исходя из заданной даты
    start = utils.get_start_for_period(work_date, type_of_period)
    work_date = datetime.datetime.strptime(work_date, "%d.%m.%Y %H:%M:%S")
    print()
    print(f'Период выборки: с {start} до {work_date}')
    print()

    # Преобразовываем столбец "Дата операции" из формата str в столбец с объектами datetime
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)

    # Фильтруем исходный датафрейм по заданному периоду и отрицательной сумме операции (платежи)
    filtered_df = df[(start <= df['Дата операции'])
        & (df['Дата операции'] <= work_date)
        & (df['Сумма операции'] < 0)
        ]

    # Определяем общую сумму платежей за период
    total_payments = int(filtered_df['Сумма операции'].apply(lambda x: abs(x) if x < 0 else 0).sum())
    print(f'Общая сумма платежей за период выборки: {total_payments} руб.')
    print()


    # Группируем расходы по категориям
    spending_by_categories = filtered_df.groupby('Категория', observed=False)

    # Определяем сумму расходов по категориям в заданном периоде
    result = spending_by_categories['Сумма операции'].apply(lambda x: x[x < 0].abs().sum())

    # Сортируем результат группировки по убыванию
    sorted_result = result.sort_values(ascending=False)

    # Выделяем основные категории (7 позиций), округляем сумму по категориям до целых чисел
    top_7 = sorted_result.head(7).astype(int)

    # Суммируем категории, не попавшие в top_7, в категорию "Остальное", округляем сумму до целого числа
    others = pd.Series({'Остальное': sorted_result.iloc[7:].sum().astype(int)})

    # Объединяем в итоговый датафрейм
    total_df = pd.concat([top_7, others])

    return total_df


if __name__ == '__main__':
    df = pd.read_excel('operations.xlsx')
    print(spending_by_period(df, '31.12.2021 23:59:59', 'Y'))
