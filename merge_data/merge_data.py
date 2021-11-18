# %%
import re
import numpy as np
import datatable
import pandas as pd
pd.set_option('display.max_columns', None)
# %%
csv_target = datatable.fread('./data_2/HP_20160702_20201231.csv').to_pandas()
csv_quest = datatable.fread('./data_2/QUESAT_DATA.csv').to_pandas()

# %%
csv_target = csv_target.drop('C0', axis='columns')
csv_quest = csv_quest.drop('C0', axis='columns')

# %%

csv = pd.merge(csv_target, csv_quest, how='left', 
                left_on=['환자번호#1', '처방일자#3'], 
                right_on=['환자번호#1', 'SM_DATE'])

# %%
csv_for_col = pd.read_csv('./data_2/HP_2001_2010_filterd.csv', index_col=0)

# %%
csv.columns = csv_for_col.columns
# %%
csv.to_csv('./data_2/HP_20160702_20201231_merged.csv')
# %%
