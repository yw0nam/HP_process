# %%
from utils import *
import re
import numpy as np
import pandas as pd
import datatable
pd.set_option('display.max_columns', None)

# %%

csv = pd.read_csv('./data/apply_exclusion.csv', index_col=0)
csv.head()
# %% [markdown]

# Group_1 -> HP 제균치료된 환자
csv_fd = csv[csv['TRT_HELICO_PYLORI#160'] == 1]
csv_fe = csv[csv['STATUS_HELICO_PYLORI#161'].isin([1, 2])]
# %% [markdown]