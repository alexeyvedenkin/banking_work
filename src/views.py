import datetime
import json
import logging
import os
from typing import Any, Dict

import pandas as pd
from pandas import DataFrame

from config import DATA_DIR, LOGS_DIR, RESULT_DIR
from src import utils

logger = logging.getLogger("views")
logger.setLevel(logging.DEBUG)
log_file_path = os.path.join(LOGS_DIR, 'views.log')
file_handler = logging.FileHandler(log_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


operations_path = os.path.join(DATA_DIR, 'operations.xlsx')
logger.info("Задан путь для чтения файла с данными")
df = pd.read_excel(operations_path)
logger.info("Данные из файла .xslx преобразованы в DataFrame")


def transactions_by_period(df: DataFrame, work_date: datetime, type_of_period: str = 'M') -> Dict:
    """Возвращает общую сумму расходов за период
    """
    total_result = {}
    expenses_dict = {}

    # Определяем период для обработки исходя из заданной даты
    start = utils.get_start_for_period(work_date, type_of_period)
    work_date = datetime.datetime.strptime(work_date, "%d.%m.%Y %H:%M:%S")
    print()
    print(f'Период выборки: с {start} до {work_date}')
    print()

    # Преобразовываем столбец "Дата операции" из формата str в столбец с объектами datetime
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)

    # Фильтруем исходный датафрейм по заданному периоду и отрицательной сумме операции (платежи)
    filtered_df_for_spending = df[(start <= df['Дата операции']) & (df['Дата операции'] <= work_date)
                                  & (df['Сумма операции'] < 0)]

    # Определяем общую сумму платежей за период
    total_payments = (
        int(filtered_df_for_spending['Сумма операции'].apply(lambda x: abs(x) if x < 0 else 0).sum().astype(int)))
    print(f'Общая сумма платежей за период выборки: {total_payments} руб.')
    print()

    # Группируем датафрейм по категориям
    grouped_by_categories_spending = filtered_df_for_spending.groupby('Категория', observed=False)

    # Определяем сумму расходов по категориям в заданном периоде, округляем сумму до целого числа
    result_spending = (
        grouped_by_categories_spending['Сумма операции'].apply(lambda x: x[x < 0].abs().sum().astype(int)))

    # Сумма по категории "Переводы":
    total_transfers = int(result_spending['Переводы']) if 'Переводы' in result_spending.index else 0
    # print('total_transfers:', total_transfers)
    # print()

    # Сумма по категории "Наличные":
    total_cash = int(result_spending['Наличные']) if 'Наличные' in result_spending.index else 0
    # print('total_cash:', total_cash)
    # print()

    # Формируем список словарей для выгрузки в JSON-файл
    transfers_and_cash = []
    transfers = {'category': 'Переводы', 'amount': total_transfers}
    transfers_and_cash.append(transfers)
    cash = {'category': 'Наличные', 'amount': total_cash}
    transfers_and_cash.append(cash)
    # print(transfers_and_cash)
    # print()

    # Сортируем результат группировки по убыванию
    sorted_result_spending = result_spending.sort_values(ascending=False)

    # Выделяем основные категории (7 позиций), округляем сумму по категориям до целых чисел
    top_7 = sorted_result_spending.head(7).astype(int)

    # Суммируем категории, не попавшие в top_7, в категорию "Остальное"
    others = pd.Series({'Остальное': sorted_result_spending.iloc[7:].sum()})

    # Объединяем платежи по категориям в итоговый датафрейм
    total_spending = pd.concat([top_7, others])
    print("Общая сумма платежей по категориям за период выборки:")
    print(total_spending)
    print()

    # Формируем словарь словарей для выгрузки в JSON
    spending_result = []
    total_info = total_spending.to_dict()
    for category, amount in total_info.items():
        spending_result.append({'category': category, 'amount': amount})

    # Фильтруем исходный датафрейм по заданному периоду и положительной сумме операции (поступления)
    filtered_df_for_incomes = df[(start <= df['Дата операции']) & (df['Дата операции'] <= work_date)
                                 & (df['Сумма операции'] > 0)]

    # Определяем общую сумму поступлений за период
    total_incomes = int(filtered_df_for_incomes['Сумма операции'].apply(lambda x: x if x > 0 else 0).sum().astype(int))
    print(f'Общая сумма поступлений за период выборки: {total_incomes}')
    print()

    # Группируем датафрейм по категориям
    grouped_by_categories_incomes = filtered_df_for_incomes.groupby('Категория', observed=False)

    # Определяем сумму поступлений по категориям в заданном периоде, округляем сумму до целого числа
    result_incomes = grouped_by_categories_incomes['Сумма операции'].apply(lambda x: x[x > 0].abs().sum().astype(int))

    # Сортируем результат группировки по убыванию
    sorted_result_incomes = result_incomes.sort_values(ascending=False)
    print(sorted_result_incomes)
    print()

    # Формируем словарь словарей для выгрузки в JSON-файл
    main_income: Any = {}
    main_income['total_amount'] = total_incomes
    incomes_result = []
    incomes_by_category = sorted_result_incomes.to_dict()
    for category, amount in incomes_by_category.items():
        incomes_result.append({'category': category, 'amount': amount})

    main_income['main'] = incomes_result

    # Формируем сводный словарь словарей для выгрузки в JSON-файл
    expenses_dict['total_amount'] = total_payments
    expenses_dict['main'] = spending_result
    expenses_dict['transfers_and_cash'] = transfers_and_cash
    total_result['expenses'] = expenses_dict
    total_result['income'] = main_income

    return total_result


def complete_result(df: DataFrame, work_date: str, type_of_period: str = 'M') -> Any:
    final_result = transactions_by_period(df, work_date, type_of_period)
    user_settings_path = os.path.join(DATA_DIR, 'user_settings.json')
    curr_data = utils.request_currency(user_settings_path)
    stock_data = utils.stock_indices(user_settings_path)
    final_result['currency_rates'] = curr_data
    final_result['stock_prices'] = stock_data
    complete_path = os.path.join(RESULT_DIR, 'views.json')
    with open(complete_path, 'w', encoding='utf-8') as file:
        json.dump(final_result, file, indent=4, ensure_ascii=False)

    return final_result
