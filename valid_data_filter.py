# %%
import re
import numpy as np
import datatable
import pandas as pd
from utils import *
pd.set_option('display.max_columns', None)
# %%
data = pd.read_csv('./data_2/selected_data.csv', index_col=0)
# %% [markdown]
# # 총 N수 45207개
data

# %% 
# %% [markdown]
# # 제외기준 2 위수술이력 문진 == 1 -> N수 137개
# %%
csv_surgery_stomach = data[data['SURGERY_STOMACH#138'] == 1]

# %% [markdown]
# 내시경 STG, TG 포함일 경우 -> 텍스트 검출로 확인 -> N수 97개
# %% 
csv_7 = data.copy()
# map_fn: 검사결과내용#7의 값이 string이 아닌 Row를 제거
csv_7['검사결과내용#7_process'] = csv_7['검사결과내용#7'].map(lambda x: map_fn(x))
csv_7 = csv_7[csv_7['검사결과내용#7_process'] != 0]

p = re.compile('gastrectomy')
idx = find_index(csv_7, p)
csv_7 = data[data.index.isin(idx)]
# %%
#제외기준 3 가족중 위장암존재 -> N수 4445개
csv_3 = data[(data['FAMILY_CANCER_STOMACH_F#170'] == 1) | 
              (data['FAMILY_CANCER_STOMACH_M#171'] == 1) |
              (data['FAMILY_CANCER_STOMACH_SIB#172'] == 1) |
              (data['FAMILY_CANCER_STOMACH_CH#173'] == 1)]

# %%
# 제외기준 4 성별, 연령 없는경우 -> N수 0개
csv_4 = data[(data['처방일자{연령}#4'].isna()) | 
        (data['성별#8'].isna())]
# %%

csv_1st = pd.read_csv('./data_2/HP_2001_2020_drug_1st.csv')
csv_1st['res'] = 1
csv_2nd = pd.read_csv('./data_2/HP_2001_2020_drug_2nd.csv')
csv_2nd['res'] = 1
# %%
csv_drug_1 = pd.merge(data, csv_1st, how='left', 
                left_on=['환자번호#1'], 
                right_on=['환자번호#1'])
# %%
csv_drug_2 = pd.merge(data, csv_2nd, how='left', 
                left_on=['환자번호#1'], 
                right_on=['환자번호#1'])

# %%

csv_drug_2['res'].value_counts()
# %%
pd.rename()
# %%

# %%
csv_1st
# %%
