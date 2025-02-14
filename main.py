import os
from src import utils


read_file = utils.read_excel('data/operations.xlsx')
print(*read_file[:5], sep='\n')