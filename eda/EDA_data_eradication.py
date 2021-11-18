# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tableone import TableOne
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
pd.set_option('display.max_columns', None)
# %%
eradication_csv_1 = pd.read_csv("./data/HP_drug_1_unlock.csv", 
                              index_col=0, encoding='CP949')
eradication_csv_2 = pd.read_csv("./data/HP_drug_2_unlock.csv", 
                              index_col=0, encoding='CP949')
# %%
eradi_csv = pd.merge(eradication_csv_1[['환자번호#1', '처방일자#3']], eradication_csv_2[['환자번호#1', '처방일자#3']], 
                     how='left', left_on='환자번호#1', right_on='환자번호#1')
eradi_csv.columns = ['환자번호', '제균처방일자_1', '제균처방일자_2']
# %%
min_date = []
for patient in eradi_csv['환자번호'].value_counts().index:
   print(patient)
   temp = eradi_csv.query("환자번호 == @patient")
   
   min_date.append(min(temp['제균처방일자_1'].min(), temp['제균처방일자_2'].min()))
# %%
csv = pd.read_csv('./data_for_analysis/hp_bx.fu365.fu_cdw.csv')
csv['처방일자'] = pd.to_datetime(csv['처방일자'])
csv['first_fu'] = pd.to_datetime(csv['first_fu'])
csv['last_fu'] = pd.to_datetime(csv['last_fu'])

# %%
csv = pd.merge(csv, eradi_csv, how='left', left_on='환자번호', right_on='환자번호_1')
# %%
