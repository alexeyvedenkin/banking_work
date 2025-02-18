# import csv
import datetime
import logging
import os
from typing import Any
from dateutil.relativedelta import relativedelta
from datetime import timedelta

# import pandas as pd

utils_logger = logging.getLogger('utils')
utils_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs/utils.log', "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)

#
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


def filter_by_date(my_lst: list[dict], start: str, stop: str) -> list[dict]:
    """Возвращает список словарей, отфильтрованный по дате
    """
    pass


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


def get_start_for_period(work_date: str, type_of_period: str) -> datetime.datetime:
    """Возвращает начало периода выборки по заданному критерию для заданной даты
    """
    work_datetime = datetime.datetime.strptime(work_date, "%Y-%m-%d %H:%M:%S")
    if type_of_period == 'W':
        start_of_period = get_start_of_week(work_datetime)
    elif type_of_period == 'M':
        start_of_period = get_start_of_month(work_datetime)
    elif type_of_period == 'Y':
        start_of_period = get_start_of_year(work_datetime)
    elif type_of_period == 'ALL':
        start_of_period = get_start_without_period(work_datetime)
    return start_of_period


def get_start_of_week(work_date: datetime.datetime) -> datetime.datetime:
    # Определяем дату начала недели
    start_of_week = work_date - timedelta(days=work_date.weekday())
    # Устанавливаем время начала недели на 00:00:00
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_week


def get_start_of_month(work_date: datetime.datetime) -> datetime.datetime:
    # Определяем дату начала месяца
    start_of_month = datetime.datetime(work_date.year, work_date.month, 1)
    # Устанавливаем время начала месяца на 00:00:00
    start_of_month = start_of_month.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_month


def get_start_of_year(work_date: datetime.datetime) -> datetime.datetime:
    # Определяем дату начала года
    start_of_year = datetime.datetime(work_date.year, 1, 1)
    # Устанавливаем время начала года на 00:00:00
    start_of_year = start_of_year.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_year


def get_start_without_period(work_date: datetime.datetime) -> datetime.datetime:
    # Определяем дату начала отбора # 0001-01-01
    start_of_all = datetime.datetime(1, 1, 1)
    # Устанавливаем время начала отбора на 00:00:00
    start_of_all = start_of_all.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_all


# # Заданная дата
# date = datetime(2025, 2, 18, 14, 15, 16)
#
# # Вычислить начало недели
# start_of_week = get_start_of_week(date)



if __name__ == '__main__':
    # print(*read_csv("transactions.csv")[:5], sep='\n')
    # print()
    # print(read_excel('operations.xlsx'), sep='\n')
    # print(pd.read_excel("operations.xlsx")[:5], sep='\n')
    # df = pd.read_excel('operations.xlsx', usecols=[0, 4, 9, 11])
    # print(df[:20])
    print(get_start_for_period('2025-02-18 22:54:00', 'W'))
    print(get_start_for_period('2025-02-18 22:54:00', 'M'))
    print(get_start_for_period('2025-02-18 22:54:00', 'Y'))
    print(get_start_for_period('2025-02-18 22:54:00', 'ALL'))

