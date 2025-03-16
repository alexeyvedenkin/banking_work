# import datetime
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any

import requests
from dotenv import load_dotenv
from requests import HTTPError

from config import DATA_DIR, LOGS_DIR

utils_logger = logging.getLogger('utils')
utils_logger.setLevel(logging.DEBUG)
log_file_path = os.path.join(LOGS_DIR, 'utils.log')
file_handler = logging.FileHandler(log_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)

load_dotenv()


# def read_excel(filename: str) -> Any:
#     """
#     Считывает файл в формате xlsx и возвращает данные в виде списка словарей
#     """
#
#     if not os.path.exists(filename):
#         utils_logger.error("File not found")
#         return []  # Return an empty list in case of error
#     utils_logger.info("Начало загрузки Excel файла")
#     reading_excel = read_excel(filename)
#     # Convert DataFrame to list of dictionaries
#     transactions_list = reading_excel.to_dict("records")
#     utils_logger.info("Окончание загрузки Excel файла")
#
#     return transactions_list


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
    work_datetime = datetime.strptime(work_date, "%d.%m.%Y %H:%M:%S")
    if type_of_period == 'W':
        # Определяем дату начала недели
        offset = (work_datetime.weekday() - 0) % 7
        work_datetime = work_datetime - timedelta(days=offset)
        return work_datetime.replace(hour=0, minute=0, second=0)
        # return work_datetime.replace(day=1, hour=0, minute=0, second=0)
    elif type_of_period == 'M':
        # Определяем дату начала месяца
        # start_by_period = get_start_of_month(work_datetime)
        return work_datetime.replace(day=1, hour=0, minute=0, second=0)
    elif type_of_period == 'Y':
        # Определяем дату начала года
        # start_by_period = get_start_of_year(work_datetime)
        return work_datetime.replace(month=1, day=1, hour=0, minute=0, second=0)
    elif type_of_period == 'ALL':
        # start_by_period = get_start_without_period(work_datetime)
        return datetime(1971, 1, 1, 0, 0, 0)
    else:
        raise ValueError("Некорректно задана дата")
    # return start_by_period


# def get_start_of_week(work_date: datetime) -> Any:
#     # Определяем дату начала недели
#     start_of_week = work_date - timedelta(days=work_date.weekday())
#     # Устанавливаем время начала недели на 00:00:00
#     start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
#     return start_of_week
#
#
# def get_start_of_month(work_date: datetime) -> Any:
#     # Определяем дату начала месяца
#     start_of_month = datetime.datetime(work_date.year, work_date.month, 1)
#     # Устанавливаем время начала месяца на 00:00:00
#     start_of_month = start_of_month.replace(hour=0, minute=0, second=0, microsecond=0)
#     return start_of_month
#
#
# def get_start_of_year(work_date: datetime) -> Any:
#     # Определяем дату начала года
#     start_of_year = datetime.datetime(work_date.year, 1, 1)
#     # Устанавливаем время начала года на 00:00:00
#     start_of_year = start_of_year.replace(hour=0, minute=0, second=0, microsecond=0)
#     return start_of_year


# def get_start_without_period(work_date: datetime) -> Any:
#     # Определяем дату начала отбора # 1971-01-01
#     start_of_all = datetime.datetime(1971, 1, 1)
#     # Устанавливаем время начала отбора на 00:00:00
#     # start_of_all = start_of_all.replace(hour=0, minute=0, second=0, microsecond=0)
#     return start_of_all


# def get_names_of_currency_and_stocks(filename: str='user_settings.json') -> Any:
#     """ Получает данные из внешнего JSON-файла и преобразовывает в объект Python
#     """
#     path = os.path.join(DATA_DIR, filename)
#     utils_logger.debug('Получение пути к файлу с данными')
#     if not os.path.exists(path):
#         utils_logger.error('Не задан путь к исходным данным')
#         print('Не задан путь')
#         return []
#     with open(path, encoding="utf-8") as file_json:
#         utils_logger.info('Получение данных из исходного файла')
#         data_json = json.load(file_json)
#         utils_logger.info('Полученные данные преобразованы в объект Python')
#     return data_json


def request_currency(filename: str = 'user_settings.json') -> list[dict]:
    """Запрашивает на API-сервисе курсы валют, заданных пользователем, и возвращает результат запроса
    """
    utils_logger.info('Получение данных из исходного файла')
    path = os.path.join(DATA_DIR, filename)
    utils_logger.debug('Получение пути к файлу с данными')
    if not os.path.exists(path):
        utils_logger.error('Не задан путь к исходным данным')
        print('Не задан путь')
        return []
    with open(path, encoding="utf-8") as file_json:
        utils_logger.info('Получение данных из исходного файла')
        data_json = json.load(file_json)
        utils_logger.info('Полученные данные преобразованы в объект Python')
    currency_list = data_json.get('user_currencies', 'Нет данных')
    utils_logger.info('Получены данные из исходного файла')
    utils_logger.debug('Присвоено значение apikey из для получения данных из .env')
    apikey = os.getenv('APIKEY_EXCHANGERATE')
    if not apikey:
        print("Ошибка: API ключ не найден. Убедитесь, что он задан в .env файле.")
        return []

    headers = {"apikey": f"{apikey}"}

    currency_rates = []
    for currency in currency_list:
        url = f"https://v6.exchangerate-api.com/v6/{apikey}/pair/{currency}/RUB"
        response = requests.get(url, headers=headers)
        try:
            response.raise_for_status()
        except HTTPError:
            utils_logger.error('Некорректный ответ от API')
            continue
        data = response.json()
        utils_logger.debug('Получен корректный ответ от API')
        currency_course = {'currency': currency, 'rate': round(float(data['conversion_rate']), 2)}
        currency_rates.append(currency_course)
        utils_logger.debug('Записан курс валюты в итоговый список')
    return currency_rates


def stock_indices(filename: str = 'user_settings.json') -> list[dict]:
    """Запрашивает на API-сервисе курсы акций, заданных пользователем, и возвращает результат запроса
    """
    utils_logger.info('Получение данных из исходного файла')
    path = os.path.join(DATA_DIR, filename)
    utils_logger.debug('Получение пути к файлу с данными')
    if not os.path.exists(path):
        utils_logger.error('Не задан путь к исходным данным')
        print('Не задан путь')
        return []
    with open(path, encoding="utf-8") as file_json:
        utils_logger.info('Получение данных из исходного файла')
        data_json = json.load(file_json)
        utils_logger.info('Полученные данные преобразованы в объект Python')
    stock_list = data_json.get('user_stocks', 'Нет данных')
    utils_logger.info('Получены данные из исходного файла')
    utils_logger.debug('Присвоено значение apikey из для получения данных из .env')
    apikey = os.getenv('APIKEY_TWELVEDATA_STOCK')
    if not apikey:
        print("Ошибка: API ключ не найден. Убедитесь, что он задан в .env файле.")
        return []

    headers = {"apikey": f"{apikey}"}

    stock_prices = []
    for stock in stock_list:
        url = f"https://api.twelvedata.com/eod?symbol={stock}&interval=1min&apikey={apikey}"
        response = requests.get(url, headers=headers)
        try:
            response.raise_for_status()
        except HTTPError:
            utils_logger.error('Некорректный ответ от API')
            continue

        data = response.json()
        utils_logger.debug('Получен корректный ответ от API')
        if 'close' in data:
            stock_price = {'stock': stock, 'price': round(float(data['close']), 2)}
            utils_logger.debug('Записана котировка акции в итоговый список')
            stock_prices.append(stock_price)

    return stock_prices


# def greeting() -> Any:
#     current_date_time = datetime.datetime.now()
#     if 5 <= current_date_time.hour < 11:
#         greet = 'Доброе утро'
#     elif 11 <= current_date_time.hour < 17:
#         greet = 'Добрый день'
#     elif 17 <= current_date_time.hour < 23:
#         greet = 'Добрый вечер'
#     else:
#         greet = 'Доброй ночи'
#
#     print(f'Текущее время: {current_date_time}')
#     print()
#
#     return f'{greet}, уважаемый пользователь!'


# if __name__ == '__main__':
    # print(*read_csv("transactions.csv")[:5], sep='\n')
    # print()
    # operations_path = os.path.join(DATA_DIR, 'operations.xlsx')
    # print(read_excel(operations_path), sep='\n')
    # print(pd.read_excel(operations_path)[:5], sep='\n')
    # df = pd.read_excel('operations.xlsx', usecols=[0, 4, 9, 11])
    # print(df[:20])
    # print(get_start_for_period('18.02.2025 22:54:00', 'W'))
    # print(get_start_for_period('18.02.2025 22:54:00', 'M'))
    # print(get_start_for_period('18.02.2025 22:54:00', 'Y'))
    # print(get_start_for_period('18.02.2025 22:54:00', 'ALL'))
    # print(get_names_of_currency_and_stocks('user_settings.json'))
    # user_settings_path = os.path.join(DATA_DIR, 'user_settings.json')
    # print(*stock_indices(user_settings_path), sep='\n')
    # print(*request_currency(user_settings_path), sep='\n')
    # print(greeting(dt.datetime.now()))
    # print(get_start_of_week(datetime.datetime.strptime('31.03.2021 23:59:59', "%d.%m.%Y %H:%M:%S")))
