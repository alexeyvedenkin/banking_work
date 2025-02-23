import datetime
import json
import logging
import os
from typing import Dict
from config import LOGS_DIR, DATA_DIR, RESULT_DIR
import pandas as pd

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
# # Загрузка переменных окружения из .env файла
# load_dotenv()
#
# # Получение значения переменной API_KEY из .env-файла
# # apikey = os.getenv('APIKEY_FINNHUB')


# def main_page():
#     """Возвращает JSON-ответ по настройкам
#     """
#     pass
#
#
# def events_page():
#     """Возвращает JSON-ответ по настройкам
#     """
#     pass


def transactions_by_period(df, work_date: str, type_of_period: str = 'M') -> Dict:
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

    # Формируем словарь словарей для выгрузки в JSON-файл
    # total_result = {'expenses': {'total_amount': total_payments}}
    # print(total_result)
    # print()

    # Группируем датафрейм по категориям
    grouped_by_categories_spending = filtered_df_for_spending.groupby('Категория', observed=False)

    # Определяем сумму расходов по категориям в заданном периоде, округляем сумму до целого числа
    result_spending = (
        grouped_by_categories_spending['Сумма операции'].apply(lambda x: x[x < 0].abs().sum().astype(int)))
    # print(result_spending, type(result_spending))
    # print()

    # transfers_and_cash = result_spending[result_spending.loc in ['Переводы', 'Наличные']]
    # print(transfers_and_cash)

    # Сумма по категории "Переводы":
    total_transfers = int(result_spending['Переводы'])
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

    # total_spending_df = total_spending.set_index('index').to_dict(orient='index')
    # total_spending_df = pd.DataFrame.to_dict(total_spending)   # columns=['category', 'amount'])
    # total_spending_df.set_index('index').to_dict(orient='index')
    # # Присвоение имен столбцам
    # print(total_spending_df.head(7), type(total_spending_df))
    # print()
    # total_spending_df.columns = ['category', 'amount']

    # Формируем список словарей для выгрузки в JSON-файл
    # main_payments = total_spending_df.set_index('index').to_dict(orient='index')
    # print(main_payments)
    # print()

    # Фильтруем исходный датафрейм по заданному периоду и положительной сумме операции (поступления)
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

    # sorted_result_incomes_df = sorted_result_incomes.reset_index()

    # Формируем словарь словарей для выгрузки в JSON-файл
    main_income = {}
    main_income['total_amount'] = total_incomes
    incomes_result = []
    incomes_by_category = sorted_result_incomes.to_dict()
    for category, amount in incomes_by_category.items():
        incomes_result.append({'category': category, 'amount': amount})

    main_income['main'] = incomes_result
    # print(main_income, type(main_income))

    # main_incomes = sorted_result_incomes_df.set_index('index').to_dict(orient='index')
    # print(main_incomes)
    # print()

    # Формируем сводный словарь словарей для выгрузки в JSON-файл
    expenses_dict['total_amount'] = total_payments
    expenses_dict['main'] = spending_result
    expenses_dict['transfers_and_cash'] = transfers_and_cash
    total_result['expenses'] = expenses_dict
    total_result['income'] = main_income
    # print(total_result)

    return total_result  # result_incomes


def complete_result(*args, **kwargs):
    final_result = transactions_by_period(df, work_date='31.12.2021 23:59:59')
    user_settings_path = os.path.join(DATA_DIR, 'user_settings.json')
    curr_data = utils.request_currency(user_settings_path)
    stock_data = utils.stock_indices(user_settings_path)
    final_result['currency_rates'] = curr_data
    final_result['stock_prices'] = stock_data
    complete_path = os.path.join(RESULT_DIR, 'views.json')
    with open(complete_path, 'w', encoding='utf-8') as file:
        json.dump(final_result, file, indent=4, ensure_ascii=False)

    return final_result

# # Создание заголовка с токеном доступа API
# headers = {"apikey": f"{apikey}"}


# def read_currency_and_stocks(path: str) -> Any:
#     """Получает данные о курсах валют с API-ресурса и возвращает в формате dict{dict}
#     """
#     if not os.path.exists(path):
#         logger.error('Не задан путь к исходным данным')
#         return []
#     with open(path, encoding="utf-8") as file_json:
#         logger.info('Получение данных из исходного файла')
#         data_json = json.load(file_json)
#         logger.info('Полученные данные преобразованы в объект Python')
#         # print(*data_json, end='\n')
#     return data_json
    # if "operationAmount" not in transaction:
    #     print("Ошибка: ключ 'operationAmount' отсутствует в транзакции")
    #     return 0.0
    #
    # amount = float(transaction["operationAmount"]["amount"])  # получение суммы траты

    # parsed_data = json.loads(data.user_settings.json)
    # currency = [x for x in data.user_settings.json["user_currencies": ["USD", "EUR"]]  # получение валюты
    #
    # if currency != "RUB":
    #     apikey = os.getenv("API_KEY")
    #
    #     if not apikey:
    #         print("Ошибка: API ключ не найден. Убедитесь, что он задан в .env файле.")
    #         return 0.0
    #
    #     # url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from{currency}&amount={amount}"
    #
    #     headers = {"apikey": f"{apikey}"}
    #
    #     response = requests.get(url, headers=headers)
    #     response_data = response.json()
    #
    #     # Отладочная информация
    #     print(f"Запрос: {url}")
    #     print(f"Статус ответа: {response.status_code}")
    #     print(f"Ответ: {response_data}")
    #
    #     try:
    #         return round(response_data["result"], 2)
    #     except KeyError:
    #         print("Ошибка: ключ 'result' отсутствует в ответе API")
    #         return 0.0
    #
    # # return amount


# if __name__ == '__main__':
    # print(utils.greeting())
    # operations_path = os.path.join(DATA_DIR, 'operations.xlsx')
    # df = pd.read_excel(operations_path)
    # # print(transactions_by_period(df, '31.12.2021 23:59:59', 'Y'))
    # print(*complete_result(), sep='\n')
