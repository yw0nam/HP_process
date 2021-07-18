# %%
import re
import numpy as np
import datatable
import pandas as pd
from utils import *
pd.set_option('display.max_columns', None)
# %%
data = pd.read_csv('./data_2/selected_data.csv', index_col=0)
# data = pd.read_csv('./data_2/final_data.csv', index_col=0)
# %% [markdown]

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