import datetime
import logging
import os

import pandas as pd

from config import DATA_DIR, LOGS_DIR, RESULT_DIR
from src import reports, services, views

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
log_file_path = os.path.join(LOGS_DIR, 'main.log')
file_handler = logging.FileHandler(log_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


work_date = "31.03.2021 23:59:59"
now_date = datetime.datetime.now()
operations_path = os.path.join(DATA_DIR, 'operations.xlsx')
df = pd.read_excel(operations_path)
data = df.to_dict('records')

print()
logger.info("Выведено приветствие")
# print(utils.greeting())
print()
print('Результат работы страницы "События":')
logger.info("Начало вывода результатов")
print(*views.complete_result(df, work_date, 'W'), sep='\n')
print()
logger.info("Получен путь для выгрузки")
views_path = os.path.join(RESULT_DIR, 'views.json')
logger.info("Результат выгружен в json-файл")
print('Результат записан в файл results\\views.json')
logger.info("Окончание работы страницы События")
print()
logger.info("Начало работы файла services.py")
print('Результат работы функции find_people_pass (Переводы физическим лицам):')
print()
print('Формат результирующих данных (выведено первые 5 записей c переводами физическим лицам):')
logger.info("Заголовок результата выведен в консоль")
services.find_people_pass(data)
logger.info("Получен путь для выгрузки")
people_pass_path = os.path.join(RESULT_DIR, 'people_pass.json')
logger.info("Результат выгружен в json-файл")
print('Результат записан в файл results\\people_pass.json')
print()
logger.info("Окончание работы файла services.py")
print()
logger.info("Начало работы файла reports.py")
print('Результат работы функции spending_by_weekday:')
print()
logger.info("Результат выведен в консоль")
print(reports.spending_by_weekday(df, '31.03.2021 23:59:59'))
logger.info("Результат выгружен в JSON")
print('Результат работы функции записан в файл results/reports.json')
