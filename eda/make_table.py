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
data_name = 'any_bx'
save_path = '../images/paper_figure/2021_12_20/'
read_path = '../data_with_family_hx/'
csv = pd.read_csv(read_path+'%s.cov.fillna_cancer.up_death.final_fu.add_fu.cancer_stage.csv'%(data_name))
if data_name == 'any_bx':
    t = pd.read_csv(read_path+'bx_for_hp.cov.fillna_cancer.up_death.final_fu.add_fu.cancer_stage.csv')
    t['bx_for_hp'] = 1
    csv = pd.merge(csv, t[['환자번호', 'bx_for_hp']], how='left',
         left_on='환자번호', right_on='환자번호')
    csv['bx_for_hp'] = csv['bx_for_hp'].fillna(0)
    del t
# %%
csv['사망여부'] = csv['사망여부'].replace({'N':0, 'Y':1})
csv['사망여부'] = csv['사망여부'].fillna(0).astype(int)
csv['cancer_fu'] = csv['cancer_fu'].replace({'N':0, 'Y':1})
csv['cancer_fu'] = csv['cancer_fu'].fillna(0).astype(int)
csv['cancer_stage'] = csv['cancer_stage'].fillna('None')
# %%
csv['처방일자'] = pd.to_datetime(csv['처방일자'])
csv['final_fu_death'] = pd.to_datetime(csv['final_fu_death'])
csv['cancer_fu_date'] = pd.to_datetime(csv['cancer_fu_date'])
csv['first_fu'] = pd.to_datetime(csv['first_fu'])
csv['index_date'] = pd.to_datetime(csv['index_date'])
# %%
csv['group'] = csv['group'].replace({3:1, 4:2})
csv['cancer_fu_duration'] = (csv['cancer_fu_date'] - csv['index_date']).map(lambda x: x.days)
csv['death_fu_duration'] = (csv['final_fu_death'] - csv['index_date']).map(lambda x: x.days) 
csv = csv.drop('cancer', axis=1)
csv = csv.rename({'사망여부':'death', 'cancer_fu':'cancer'}, axis=1)
# %%
csv['EGD'] = csv['EGD'].replace({'WNL': 0, 'CAG': 1, 'MG':2, 'CSG': 0, 'LFG':0})
# %%
data = pd.read_csv('./../data_with_family_hx/apply_exclusion.csv')
csv_family_cancer = data[(data['FAMILY_CANCER_STOMACH_F#170'] == 1) | 
              (data['FAMILY_CANCER_STOMACH_M#171'] == 1) |
              (data['FAMILY_CANCER_STOMACH_SIB#172'] == 1) |
              (data['FAMILY_CANCER_STOMACH_CH#173'] == 1)]
csv_family_cancer['family_hx'] = 'Y'
csv_family_cancer = csv_family_cancer[['환자번호#1', 'family_hx']]
csv = pd.merge(csv, csv_family_cancer, how='left', left_on='환자번호', right_on='환자번호#1')
csv = csv.drop('환자번호#1', axis=1)
csv['family_hx'] = csv['family_hx'].fillna('N')
# %%
cols = ['age', 'BMI', 'CCI', 'Hb', 'TG', 
                'HDL', 'LDL', 'glucose',
                'sex', 'smoking', 'alcohol_drinking', 
                'physical_activity', 'EGD', 'family_hx', 'cancer', 
                'death', 'death_fu_duration', 'cancer_fu_duration', 'cancer_stage']

category_cols = ['sex', 'smoking', 'alcohol_drinking', 'family_hx',
                'physical_activity', 'EGD', 'cancer', 'death', 'cancer_stage']

if data_name == 'any_bx':
    cols += ['bx_for_hp']
    category_cols += ['bx_for_hp']
mytable = TableOne(csv, columns=cols, categorical=category_cols,
                   groupby='group', pval=True, nonnormal='bili')
mytable.to_html('%s/%s_table.html'%(save_path, data_name))
# %%
mytable = TableOne(csv.query("group == 2").query("cancer == 1"), columns=cols, categorical=category_cols,
                nonnormal='bili')
mytable.to_html('%s/%s_table_natrual_regression_only_cancer.html'%(save_path, data_name))
# %%
