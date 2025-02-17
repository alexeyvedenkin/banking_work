# import os
import pandas as pd
from src import reports, utils


df = pd.read_excel('operations.xlsx')

print()
print('Результат работы функции spending_by_weekday:')
print()
print(reports.spending_by_weekday(df, '31.03.2021 23:59:59'))
