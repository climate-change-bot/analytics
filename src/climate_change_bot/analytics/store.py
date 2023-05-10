import os
import pandas as pd

_file_name = os.environ.get('FILE_NAME', '../../../data/conversations_prod.xlsx')


class GlobalStore:
    def __init__(self):
        df = pd.read_excel(_file_name)
        df = df[df.testphase != 0]  # Testphase 0 is ignored because it consists mainly of test conversations
        df.reset_index(drop=True, inplace=True)
        self.df = df

    def get_data(self, filter_value):
        if filter_value == 0:
            return self.df
        else:
            df_filtered = self.df[self.df.testphase == filter_value]
            df_filtered.reset_index(drop=True, inplace=True)
            return df_filtered

    def set_data(self, new_df):
        self.df = new_df


global_store = GlobalStore()
