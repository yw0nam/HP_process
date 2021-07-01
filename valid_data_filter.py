# %%
import re
import numpy as np
import datatable
import pandas as pd
from utils import *
pd.set_option('display.max_columns', None)
# %%
csv_1 = pd.read_csv('./data_2/HP_2001_2010_filterd.csv', index_col=0)
csv_2 = pd.read_csv('./data_2/HP_2011_20160701_filterd.csv', index_col=0)
csv_3 = pd.read_csv('./data_2/HP_20160702_20201231_filterd.csv', index_col=0)

data = pd.concat([csv_1, csv_2, csv_3])
data = data.reset_index()
data = data.drop('index', axis='columns')
# %%
data
# %%
#제외기준 2 위수술이력 문진 == 1
data = data[data['SURGERY_STOMACH#138'] != 1]

# %% 내시경 STG, TG 포함
csv_7 = data.copy()
# map_fn: 검사결과내용#7의 값이 string이 아닌 Row를 제거
csv_7['검사결과내용#7_process'] = csv_7['검사결과내용#7'].map(lambda x: map_fn(x))
csv_7 = csv_7[csv_7['검사결과내용#7_process'] != 0]

filter_string = ['subtotal gastrectomy', 'proximal gastrectomy', 'total gastrectomy', 'b-i']
index = []
for strings in filter_string:
    p = re.compile(strings)
    idx = find_index(csv_7, p)
    index = index + list(idx)

p = re.compile('TG')
csv_7['검사결과내용#7_process'] = csv_7['검사결과내용#7_process'].map(lambda x: find_text(x, p))
csv_7 = csv_7[csv_7['검사결과내용#7_process'] != 0]
indexs = list(set(index + list(csv_7.index)))

data = data[data.index.isin(indexs)]
# %%
#제외기준 3 가족중 위장암존재
data = data[data['FAMILY_CANCER_STOMACH_F#170'] != 1]
data = data[data['FAMILY_CANCER_STOMACH_M#171'] != 1]
data = data[data['FAMILY_CANCER_STOMACH_SIB#172'] != 1]
data = data[data['FAMILY_CANCER_STOMACH_CH#173'] != 1]
data

# %%
# 제외기준 4 
data = data[~data['처방일자{연령}#4'].isna()]
data = data[~data['성별#8'].isna()]
data
# %%
print(data['검사결과내용#7'][1])
# %%
