import os
import pandas as pd

_file_name = os.environ.get('FILE_NAME', '../../../data/conversations_prod.xlsx')


class GlobalStore:
    def __init__(self):
        self.df = pd.read_excel(_file_name)
        self.df['timestamp_datetime'] = pd.to_datetime(self.df['timestamp'], unit='s')
        self.df['date'] = self.df['timestamp_datetime'].dt.date

    def get_data(self, filter_value):
        if filter_value == 0:
            return self.df
        else:
            df_filtered = self.df[self.df.testphase == filter_value]
            return df_filtered

    def set_data(self, new_df):
        self.df = new_df


global_store = GlobalStore()
