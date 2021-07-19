# %%
import re
import numpy as np
import datatable
import pandas as pd
from utils import *

# testing
csv_1 = datatable.fread('./data_2/HP_2001_2010.csv').to_pandas()
csv_2 = datatable.fread('./data_2/HP_2011_20160701.csv').to_pandas()
csv_3 = datatable.fread('./data_2/HP_20160702_20201231_merged.csv').to_pandas()
# %%
csv = pd.concat([csv_1, csv_2, csv_3])
csv = csv.reset_index()
csv = csv.drop(['index', 'C0'], axis='columns')
idx = list(csv['환자번호#1'].drop_duplicates().index)
csv = csv[csv.index.isin(idx)]
csv.to_csv('./data/remove_duplicate_ori.csv')

# %%
