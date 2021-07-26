# %%
import re
import numpy as np
import datatable
import pandas as pd
from utils import *
pd.set_option('display.max_columns', None)
# %% [markdown]
# # Follow up indexes
csv = datatable.fread('./data/concated.csv').to_pandas()
csv = csv.drop('C0', axis=1)
csv['처방일자#3'] = pd.to_datetime(csv['처방일자#3'])
csv['처방일자(최초1) #101'] = pd.to_datetime(csv['처방일자(최초1) #101'])
csv['result'].dropna()
csv_fu = csv[csv['result'] >= 365]
del csv
# %%
data = pd.read_csv('./data/include_criteria.csv', index_col=0)
data = data.drop('검사결과내용#20_process', axis='columns')
# %% [markdown]
# # 총 검사수 41745개

# %% [markdown]
# # 제외기준 2 위수술이력 문진 == 1 -> 검사수 123개
csv_surgery_stomach = data[data['SURGERY_STOMACH#138'] == 1]

# %% [markdown]
# # 내시경 STG, TG 포함일 경우 -> 텍스트 검출로 확인 -> 검사수 76개
csv_endoscopy = data.copy()
# map_fn: 검사결과내용#7의 값이 string이 아닌 Row를 제거
csv_endoscopy['검사결과내용#7_process'] = csv_endoscopy['검사결과내용#7'].map(lambda x: map_fn(x))
csv_endoscopy = csv_endoscopy[csv_endoscopy['검사결과내용#7_process'] != 0]

p = re.compile('gastrectomy')
idx = find_index(csv_endoscopy, p)
csv_endoscopy = data[data.index.isin(idx)]
# %% [markdown]
# # 제외기준 3 가족중 위장암존재 -> 검사수 4031개
csv_family_cancer = data[(data['FAMILY_CANCER_STOMACH_F#170'] == 1) | 
              (data['FAMILY_CANCER_STOMACH_M#171'] == 1) |
              (data['FAMILY_CANCER_STOMACH_SIB#172'] == 1) |
              (data['FAMILY_CANCER_STOMACH_CH#173'] == 1)]

# %% [markdown]
# # 제외기준 4 성별, 연령 없는경우 -> 검사수 0개
csv_not_age_or_sex = data[(data['처방일자{연령}#4'].isna()) | 
        (data['성별#8'].isna())]
# %% [markdown]
# 제외기준에 해당하는 Row제거 -> 제거 검사수 4180개

index = list(set(list(csv_not_age_or_sex.index)) |
             set(list(csv_endoscopy.index))|
             set(list(csv_family_cancer.index)) |
             set(list(csv_surgery_stomach.index))
             )
data = data[~data.index.isin(index)]
# %% [markdown]
# Apply follow up criteria
data = data[data.index.isin(csv_fu.index)]
data.to_csv('./data/apply_exclusion.csv')