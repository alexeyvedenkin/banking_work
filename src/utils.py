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
