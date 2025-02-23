import datetime
import os
import pandas as pd
from src import reports, services, utils, views
from config import DATA_DIR, LOGS_DIR, RESULT_DIR
import logging

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
log_file_path = os.path.join(LOGS_DIR, 'main.log')
file_handler = logging.FileHandler(log_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


work_date = "18.02.2025 22:54:00"
now_date = datetime.datetime.now()
operations_path = os.path.join(DATA_DIR, 'operations.xlsx')
df = pd.read_excel(operations_path)
data = df.to_dict('records')

print()
print(utils.greeting())

print('Результат работы страницы "События"')
print()
print(*views.complete_result(), sep='\n')
print()
views_path = os.path.join(RESULT_DIR, 'views.json')
print(f'Результат записан в файл {str(views_path)}')
print()

print('Результат работы функции find_people_pass (Переводы физическим лицам):')
print()
print('Формат результирующих данных (выведено первые 5 записей c переводами физическим лицам):')
services.find_people_pass(data)
people_pass_path = os.path.join(RESULT_DIR, 'people_pass.json')
print(f'Результат записан в файл {str(people_pass_path)}')
print()

print()
print('Результат работы функции spending_by_weekday:')
print()
print(reports.spending_by_weekday(df, '31.03.2021 23:59:59'))
