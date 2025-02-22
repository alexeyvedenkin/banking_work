import datetime as dt
import json
import logging
import os
from datetime import datetime as dt_class, timedelta
from typing import Any

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

from config import DATA_DIR, LOGS_DIR
# from main import work_date


utils_logger = logging.getLogger('utils')
utils_logger.setLevel(logging.DEBUG)
log_file_path = os.path.join(LOGS_DIR, 'utils.log')
file_handler = logging.FileHandler(log_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)

load_dotenv()
#
# excel_data = pd.read_excel("data.transactions_excel.xlsx")
# print(excel_data.shape)
# print(excel_data.head())


# def read_csv(filename: str) -> list[Any] | Any:
#     """
#     Функция принимающая путь к файлу, считывает информацию c CSV файла
#     """
#     if not os.path.exists(filename):
#         logger.error("Файл не найден")
#         return []  # В случае ошибки возвращает пустой список
#     logger.info("Начало загрузки CSV файла")
#     with open(filename, encoding="utf-8") as file:
#         reading_csv = csv.DictReader(file, delimiter=";")
#         reading = [row for row in reading_csv]
#         # logger.info("Окончание загрузки CSV файла")
#         return reading


def get_work_datetime(work_datetime: str) -> Any:
    work_datetime = '31.12.2021 23:59:59'
    local_work_datetime = dt.dt_class(work_datetime)
    print('local_work_datetime', local_work_datetime)
    return local_work_datetime


def read_excel(filename: str) -> Any:
    """
    Считывает файл в формате xlsx и возвращает данные в виде списка словарей
    """

    if not os.path.exists(filename):
        utils_logger.error("File not found")
        return []  # Return an empty list in case of error
    utils_logger.info("Начало загрузки Excel файла")
    reading_excel = read_excel(filename)
    # Convert DataFrame to list of dictionaries
    transactions_list = reading_excel.to_dict("records")
    utils_logger.info("Окончание загрузки Excel файла")

    return transactions_list


# def filter_by_date(my_lst: list[dict], start: str, stop: str) -> list[dict]:
#     """Возвращает список словарей, отфильтрованный по дате
#     """
#     pass


def days_translation() -> dict:
    """Возвращает словарь для перевода дней недели из English в Russian
    """
    days_on_russian = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье'
    }
    return days_on_russian


def get_start_for_period(work_date: str, type_of_period: str) -> Any:
    """Возвращает начало периода выборки по заданному критерию для заданной даты
    """
    work_datetime = dt.datetime.strptime(work_date, "%d.%m.%Y %H:%M:%S")
    if type_of_period == 'W':
        start_by_period = get_start_of_week(work_datetime)
    elif type_of_period == 'M':
        start_by_period = get_start_of_month(work_datetime)
    elif type_of_period == 'Y':
        start_by_period = get_start_of_year(work_datetime)
    elif type_of_period == 'ALL':
        start_by_period = get_start_without_period(work_datetime)
    return start_by_period


def get_start_of_week(work_date: dt) -> Any:
    # Определяем дату начала недели
    start_of_week = work_date - timedelta(days=work_date.weekday())
    # Устанавливаем время начала недели на 00:00:00
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_week


def get_start_of_month(work_date: dt) -> Any:
    # Определяем дату начала месяца
    start_of_month = dt.datetime(work_date.year, work_date.month, 1)
    # Устанавливаем время начала месяца на 00:00:00
    start_of_month = start_of_month.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_month


def get_start_of_year(work_date: dt) -> Any:
    # Определяем дату начала года
    start_of_year = dt.datetime(work_date.year, 1, 1)
    # Устанавливаем время начала года на 00:00:00
    start_of_year = start_of_year.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_year


def get_start_without_period(work_date: dt) -> Any:
    # Определяем дату начала отбора # 0001-01-01
    start_of_all = dt.datetime(1, 1, work_date.day)
    # Устанавливаем время начала отбора на 00:00:00
    start_of_all = start_of_all.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_all


def get_names_of_currency_and_stocks(path: str) -> Any:
    """ Получает данные из внешнего JSON-файла и преобразовывает в объект Python
    """
    path = os.path.join(DATA_DIR, 'user_settings.json')
    utils_logger.debug('Получение пути к файлу с данными')
    if not os.path.exists(path):
        utils_logger.error('Не задан путь к исходным данным')
        print('Не задан путь')
        return []
    with open(path, encoding="utf-8") as file_json:
        utils_logger.info('Получение данных из исходного файла')
        data_json = json.load(file_json)
        utils_logger.info('Полученные данные преобразованы в объект Python')
        print(data_json, end='\n')
        print(type(data_json))
    return data_json


def request_currency(user_currencies: dict) -> list[dict]:
    """Запрашивает на API-сервисе курсы валют, заданных
    пользователем и возвращает результат запроса
    """
    utils_logger.info('Получение данных из исходного файла')
    user_settings_path = os.path.join(DATA_DIR, 'user_settings.json')
    currency_list = get_names_of_currency_and_stocks(user_settings_path).get('user_currencies', 'Нет данных')
    utils_logger.info('Получены данные из исходного файла')
    print(currency_list, type(currency_list))
    if "RUB" not in currency_list:
        utils_logger.debug('Проверено наличие "RUB" в исходном файле')
        utils_logger.debug('Присвоено значение apikey из для получения данных из .env')
        apikey = os.getenv('APIKEY_EXCHANGERATE')
        if apikey:
            utils_logger.debug('Прочитан APIKEY')
        else:
            utils_logger.error('НЕ прочитан APIKEY')
        print(apikey)

        if not apikey:
            print("Ошибка: API ключ не найден. Убедитесь, что он задан в .env файле.")
            return 0.0

        headers = {"apikey": f"{apikey}"}

        currency_rates = []
        for currency in currency_list:
            url = f"https://v6.exchangerate-api.com/v6/{apikey}/pair/{currency}/RUB"
            response = requests.get(url, headers=headers)
            data = response.json()
            currency_course = {}
            for key, value in data.items():
                if key in ['base_code', 'conversion_rate']:
                    if key == 'conversion_rate':
                        currency_course['rate'] = round(float(value), 2)
                    else:
                        currency_course['currency'] = value
            currency_rates.append(currency_course)

        return currency_rates


def stock_indices(user_currencies: dict) -> list[dict]:
    """Запрашивает на API-сервисе курсы акций, заданных
    пользователем, и возвращает результат запроса
    """
    utils_logger.info('Получение данных из исходного файла')
    user_settings_path = os.path.join(DATA_DIR, 'user_settings.json')
    stock_list = get_names_of_currency_and_stocks(user_settings_path).get('user_stocks', 'Нет данных')
    utils_logger.info('Получены данные из исходного файла')
    print(stock_list, type(stock_list))
    if "RUB" not in stock_list:
        utils_logger.debug('Проверено наличие "RUB" в исходном файле')
        utils_logger.debug('Присвоено значение apikey из для получения данных из .env')
        apikey = os.getenv('APIKEY_TWELVEDATA_STOCK')
        if apikey:
            utils_logger.debug('Прочитан APIKEY')
        else:
            utils_logger.error('НЕ прочитан APIKEY')
        print(apikey)

        if not apikey:
            print("Ошибка: API ключ не найден. Убедитесь, что он задан в .env файле.")
            return 0.0

        headers = {"apikey": f"{apikey}"}

        stock_prices = []
        for stock in stock_list:
            url = f"https://api.twelvedata.com/eod?symbol={stock}&interval=1min&apikey={apikey}"
            response = requests.get(url, headers=headers)
            data = response.json()

            stock_price = {}
            for key, value in data.items():
                if key in ['symbol', 'close']:
                    if key == 'close':
                        stock_price['price'] = round(float(value), 2)
                    else:
                        stock_price['stock'] = value
            stock_prices.append(stock_price)

        return stock_prices


def greeting(*args) -> Any:
    current_date_time = dt.datetime.now()
    if 6 <= current_date_time.hour < 12:
        greet = 'Доброе утро'
    elif 12 <= current_date_time.hour < 18:
        greet = 'Добрый день'
    elif 18 <= current_date_time.hour < 24:
        greet = 'Добрый вечер'
    else:
        greet = 'Доброй ночи'

    print(current_date_time)
    return f'{greet}, уважаемый пользователь!'



# def read_currency_and_stocks(path: str) -> Any:
#     """Получает данные о курсах валют с API-ресурса и возвращает в формате dict{dict}
#     """
#     if not os.path.exists(path):
#         utils_logger.error('Не задан путь к исходным данным')
#         return []
#     with open(path, encoding="utf-8") as file_json:
#         utils_logger.info('Получение данных из исходного файла')
#         data_json = json.load(file_json)
#         utils_logger.info('Полученные данные преобразованы в объект Python')
#         # print(*data_json, end='\n')
#     return data_json


if __name__ == '__main__':
    # print(*read_csv("transactions.csv")[:5], sep='\n')
    # print()
    # operations_path = os.path.join(DATA_DIR, 'operations.xlsx')
    # print(read_excel(operations_path), sep='\n')
    # print(pd.read_excel(operations_path)[:5], sep='\n')
    # df = pd.read_excel('operations.xlsx', usecols=[0, 4, 9, 11])
    # print(df[:20])
    # print(get_start_for_period('18.02.2025 22:54:00', 'W'))
    # print(get_start_for_period('2025-02-18 22:54:00', 'M'))
    # print(get_start_for_period('2025-02-18 22:54:00', 'Y'))
    # print(get_start_for_period('2025-02-18 22:54:00', 'ALL'))
    # print(get_names_of_currency_and_stocks('user_settings.json'))
    # user_settings_path = os.path.join(DATA_DIR, 'user_settings.json')
    # # print(*stock_indices(user_settings_path), sep='\n')
    # print(*request_currency(user_settings_path), sep='\n')
    print(greeting(dt.datetime.now()))
