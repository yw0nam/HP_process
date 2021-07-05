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
# %% [markdown]

# # 제균치료 이력있는경우 제외 -> N수 4619개 
csv_1st_drug = pd.read_csv('./data_2/HP_2001_2020_drug_1st.csv')
csv_1st_drug['Drug_1st_not_valid'] = 1

csv_1st_drug = csv_1st_drug[['환자번호#1', '처방일자#8', '처방코드#4', '일수(최소)#7', 
              '처방코드#9', '일수(최소)#12', '처방코드#14', '일수(최소)#17', 'Drug_1st_not_valid']]
csv_1st_drug.columns = ['환자번호#174', '처방일자#175', '처방코드#176', '일수(최소)#177', 
              '처방코드#178', '일수(최소)#179', '처방코드#180', 
              '일수(최소)#181', 'Drug_1st_not_valid#182']

csv_2nd_drug = pd.read_csv('./data_2/HP_2001_2020_drug_2nd.csv')
csv_2nd_drug['Drug_2nd_not_valid'] = 1

csv_2nd_drug = csv_2nd_drug[['환자번호#1', '처방일자#8', '처방코드#4', '일수(최소)#7', 
              '처방코드#9', '일수(최소)#12', '처방코드#14', '일수(최소)#17', 
              '처방코드#19', '일수(최소)#22', 'Drug_2nd_not_valid']]
csv_2nd_drug.columns = ['환자번호#183', '처방일자#184', '처방코드#185', '일수(최소)#186', 
              '처방코드#187', '일수(최소)#188', 
              '처방코드#189', '일수(최소)#190', 
              '처방코드#191', '일수(최소)#192', 'Drug_2nd_not_valid#193']

csv_drug = pd.merge(data, csv_1st_drug, how='left', 
                left_on=['환자번호#1'], 
                right_on=['환자번호#174'])

data = pd.merge(csv_drug, csv_2nd_drug, how='left', 
                left_on=['환자번호#1'], 
                right_on=['환자번호#183'])

csv_drug = data[(data['Drug_1st_not_valid#182'] == 1) | 
    (data['Drug_2nd_not_valid#193'] == 1)]
# %%

# %% [markdown]
# # 제외기준 2 위수술이력 문진 == 1 -> N수 137개
csv_surgery_stomach = data[data['SURGERY_STOMACH#138'] == 1]

# %% [markdown]
# # 내시경 STG, TG 포함일 경우 -> 텍스트 검출로 확인 -> N수 97개
csv_endoscopy = data.copy()
# map_fn: 검사결과내용#7의 값이 string이 아닌 Row를 제거
csv_endoscopy['검사결과내용#7_process'] = csv_endoscopy['검사결과내용#7'].map(lambda x: map_fn(x))
csv_endoscopy = csv_endoscopy[csv_endoscopy['검사결과내용#7_process'] != 0]

p = re.compile('gastrectomy')
idx = find_index(csv_endoscopy, p)
csv_endoscopy = data[data.index.isin(idx)]
# %% [markdown]
# # 제외기준 3 가족중 위장암존재 -> N수 4445개
csv_family_cancer = data[(data['FAMILY_CANCER_STOMACH_F#170'] == 1) | 
              (data['FAMILY_CANCER_STOMACH_M#171'] == 1) |
              (data['FAMILY_CANCER_STOMACH_SIB#172'] == 1) |
              (data['FAMILY_CANCER_STOMACH_CH#173'] == 1)]

# %% [markdown]
# # 제외기준 4 성별, 연령 없는경우 -> N수 0개
csv_not_age_or_sex = data[(data['처방일자{연령}#4'].isna()) | 
        (data['성별#8'].isna())]
# %% [markdown]
# 제외기준에 해당하는 Row제거 -> 제거 N수 8704개

index = list(set(list(csv_not_age_or_sex.index)) |
             set(list(csv_drug.index)) | 
             set(list(csv_endoscopy.index))|
             set(list(csv_family_cancer.index)) |
             set(list(csv_surgery_stomach.index))
             )
filtered_data = data[~data.index.isin(index)]
filtered_data.to_csv('./data_2/final_data.csv')