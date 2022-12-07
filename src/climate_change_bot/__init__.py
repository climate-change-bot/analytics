import pandas as pd
import os

file_name = os.environ.get('FILE_NAME', '../../../data/conversations_prod.xlsx')

df = pd.read_excel(file_name)
