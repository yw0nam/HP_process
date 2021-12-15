# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tableone import TableOne
import warnings
import argparse
warnings.filterwarnings("ignore", category=DeprecationWarning) 
pd.set_option('display.max_columns', None)

def define_argparser():
    p = argparse.ArgumentParser()

    p.add_argument('--folder', required=True)
    p.add_argument('--dataset_name', required=True)
    config = p.parse_args()

    return config
# %%
# config = define_argparser()
# csv = pd.read_csv('../%s/%s.cov.fillna_cancer.up_death.final_fu.csv'%(config.folder, config.dataset_name))
# %%
csv = pd.read_csv('../data_with_family_hx/bx_for_hp.cov.fillna_cancer.up_death.final_fu.csv')
print(len(csv))
csv = csv.query('group == (3, 4)')
print(len(csv))
csv['처방일자'] = pd.to_datetime(csv['처방일자'])
csv['first_fu'] = pd.to_datetime(csv['first_fu'])
csv['last_fu'] = pd.to_datetime(csv['last_fu'])
csv['final_fu_cdw'] = pd.to_datetime(csv['final_fu_cdw'])
# %%
csv['fu_1to2'] = (csv['first_fu'] - csv['처방일자']).map(lambda x: x.days)
csv['fu_1to3'] = (csv['last_fu'] - csv['처방일자']).map(lambda x: x.days)
csv['final_fu_cdw'] = csv.apply(lambda x: None if (x['first_fu'] - x['final_fu_cdw']).days > 0 else x['final_fu_cdw'], axis=1)
# %%
# Make Final Death, Cancer Follow up
csv['final_fu_cdw'] = csv['final_fu_cdw'].fillna('K')
csv['temp'] = csv['fu_dates'] + '|' +  csv['final_fu_cdw'].astype(str)
csv['temp'] = csv['temp'].map(lambda x: x.split('|')[:-1] if x.split('|')[-1] == 'K' else x.split('|'))
csv['temp'] = csv['temp'].map(lambda x: [i.split()[0] for i in x])
csv = csv[csv['temp'].map(lambda x: len(list(set(x))) >= 2)]
print(len(csv))
# %%
csv = csv.query('(fu_1to2 >= 365) or (fu_1to3 >= 365)')
print(len(csv))
# %%
def index_date_cal(baseline_fu, first_fu, last_fu):
    if (first_fu - baseline_fu).days >= 365:
        return first_fu
    elif (last_fu - baseline_fu).days >= 365:
        return last_fu
    else:
        return None
    
csv['index_date'] = csv.apply(lambda x: index_date_cal(x['처방일자'], x['first_fu'], x['last_fu']), axis=1)
 # %%
csv['final_fu_death'] = csv['사망일'].apply(lambda x: x if type(x) == str else '2021-10-12')
csv['cancer_fu'] = csv.apply(lambda x: None if x['cancer'] == 'Y' and x['cancer_date'] >= '2021-10-12' else x['cancer'], axis=1)
csv['cancer_fu_date'] = csv['cancer_date'].fillna(csv['temp'].map(lambda x: max(x))).map(lambda x: '2021-10-12' if x >= '2021-10-12' else x)
# csv = csv.drop(['temp', 'final_fu_cdw'], axis=1)
# %%
csv = csv.query('fu_1to2 <= 1895')
csv['cancer_fu_date'] = pd.to_datetime(csv['cancer_fu_date'])
csv['final_fu_death'] = pd.to_datetime(csv['final_fu_death'])
# # %%
# def check_cancer_or_death(fu, fu_date, index_date):
#     """

#     Args:
#         fu ([column]): Column that cancer or death
#         fu_date ([column]): Column that cancer or death date
#         index_date ([column]): Column that has index date.

#     """
#     if fu != 'Y':
#         return None
#     else:
#         if (fu_date - index_date).days > 0 :
#             return 'Y'
#         else:
#             return 'N'
# # %%
# # %%
# print(len(csv) - len(csv[csv.apply(lambda x: check_cancer_or_death(x['cancer_fu'],
#                                               x['cancer_fu_date'], x['index_date']), axis=1) != 'N']))
# print(len(csv) - len(csv[csv.apply(lambda x: check_cancer_or_death(x['사망여부'],
#                                               x['final_fu_death'], x['index_date']), axis=1) != 'N']))
# csv = csv[csv.apply(lambda x: check_cancer_or_death(x['cancer_fu'],
#                                               x['cancer_fu_date'],x['index_date']), axis=1) != 'N']
# csv = csv[csv.apply(lambda x: check_cancer_or_death(x['사망여부'],
#                                               x['final_fu_death'],x['index_date']), axis=1) != 'N']
# %%
print(len(csv[(csv['cancer_fu_date'] - csv['index_date']).map(lambda x: x.days) < 0]))
print(len(csv[(csv['final_fu_death'] - csv['index_date']).map(lambda x: x.days) < 0]))
# %%
# %%
csv = csv[(csv['final_fu_death'] - csv['index_date']).map(lambda x: x.days) >= 0]
csv = csv[(csv['cancer_fu_date'] - csv['index_date']).map(lambda x: x.days) >= 0]
# %%
csv = csv.rename({'BZ':'HDL'}, axis=1) 
csv['사망여부'] =csv['사망여부'].fillna('N')
csv['cancer_fu'] =csv['cancer_fu'].fillna('N')
cols = ['age', 'BMI', 'CCI', 'Hb', 'TG', 
                'HDL', 'LDL', 'glucose',
                'sex', 'smoking', 'alcohol_drinking', 
                'physical_activity', 'EGD', 'Adenoma', 'cancer_fu', '사망여부']

category_cols = ['sex', 'smoking', 'alcohol_drinking', 
                'physical_activity', 'EGD', 'Adenoma'
                 , 'cancer_fu', '사망여부']

mytable = TableOne(csv, columns=cols, categorical=category_cols,
                   groupby='group', pval=True, nonnormal='bili')
print(mytable.tabulate(tablefmt="rst"))

# %%
csv.to_csv('../%s/%s.cov.fillna_cancer.up_death.final_fu.add_fu.csv'%(config.folder, config.dataset_name), index=False)
# %%
cols = ['환자번호', '처방일자','age', 'sex', 'BMI', 
        'CCI', 'Hb', 'TG', 'HDL', 'LDL', 
        'glucose', 'smoking', 'alcohol_drinking', 'physical_activity', 'EGD', 'group']
df = csv[cols].copy()
# %%
df['first_hp_fu_date'] = csv['first_fu']
df['first_hp_fu'] = csv['first_fu_name'].map(lambda x: 'plus' if x.split('_')[1] == '3' else 'negative')
df['last_hp_fu_date'] = csv['last_fu']
df['last_hp_fu'] = csv['last_fu_name'].map(lambda x: 'plus' if x.split('_')[1] == '3' else 'negative')
df['last_fu'] = csv['temp'].map(lambda x: max(x))
# %%
data = pd.read_csv('./../data_with_family_hx/apply_exclusion.csv')
csv_family_cancer = data[(data['FAMILY_CANCER_STOMACH_F#170'] == 1) | 
              (data['FAMILY_CANCER_STOMACH_M#171'] == 1) |
              (data['FAMILY_CANCER_STOMACH_SIB#172'] == 1) |
              (data['FAMILY_CANCER_STOMACH_CH#173'] == 1)]
csv_family_cancer['family_hx'] = 'Y'
csv_family_cancer = csv_family_cancer[['환자번호#1', 'family_hx']]
df = pd.merge(df, csv_family_cancer, how='left', left_on='환자번호', right_on='환자번호#1')
df = df.drop('환자번호#1', axis=1)
# %%
df['cancer_date'] = csv.apply(lambda x: x['cancer_fu_date'] if x['cancer_fu'] == 'Y' else None, axis=1)
df['death_date'] = csv.apply(lambda x: x['final_fu_death'] if x['사망여부'] == 'Y' else None, axis=1)
# %%
df['EGD'] = df['EGD'].replace({'WNL': 0, 'CAG': 1, 'MG':2, 'CSG': 0, 'LFG':0})
# %%
# t = pd.read_excel('../data_with_family_hx/data_bx_for_hp.xlsx')
# t['bx_for_hp'] = 1
# df = pd.merge(df, t[['환자번호', 'bx_for_hp']], how='left',
#          left_on='환자번호', right_on='환자번호')
# %%
df.to_excel('../data_with_family_hx/data_bx_for_hp.xlsx', index=False)
# %%
