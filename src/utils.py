# import csv
import logging
import os
from typing import Any

import pandas as pd

logger_utils = logging.getLogger("utils")
logger_utils.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs/utils.log', "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger_utils.addHandler(file_handler)

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
    Function to read Excel file and return its content as a list of dictionaries
    """
    if not os.path.exists(filename):
        logger_utils.error("File not found")
        return []  # Return an empty list in case of error
    logger_utils.info("Начало загрузки Excel файла")
    reading_excel = pd.read_excel(filename)
    # Convert DataFrame to list of dictionaries
    transactions_list = reading_excel.to_dict("records")
    logger_utils.info("Окончание загрузки Excel файла")

    return transactions_list


if __name__ == '__main__':
    # print(*read_csv("transactions.csv")[:5], sep='\n')
    # print()
    print(*read_excel("operations.xlsx")[:5], sep='\n')
