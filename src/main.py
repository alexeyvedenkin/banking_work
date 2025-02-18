# import os
import pandas as pd
from src import reports, services


df = pd.read_excel('operations.xlsx')
data = df.to_dict('records')


print()
print('Результат работы функции find_people_pass:')
print()
print('Формат результирующих данных (выведено первые 5 записей c переводами физическим лицам):')
services.find_people_pass(data)
print('Результат записан в файл src/people_pass.json')
print()

print()
print('Результат работы функции spending_by_weekday:')
print()
print(reports.spending_by_weekday(df, '31.03.2021 23:59:59'))
