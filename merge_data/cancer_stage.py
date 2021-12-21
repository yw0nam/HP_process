# %%
import pandas as pd
import numpy as np
import warnings
import re
warnings.filterwarnings("ignore", category=DeprecationWarning) 
pd.set_option('display.max_columns', None)
# %%
cancer_stage_1 = pd.read_csv('./../etc_data/HP-암-stage-1.csv', index_col=0, encoding='CP949')
cancer_stage_2 = pd.read_csv('./../etc_data/Hp-암-stage-2-and-3.csv', index_col=0, encoding='CP949')
cancer_stage_3 = pd.read_csv('./../etc_data/HP-암-stage-4.csv', index_col=0, encoding='CP949')
# %%
cancer_stage_1 = cancer_stage_1.dropna(subset=['암T코드#10'])
cancer_stage_1['암T코드#10'] = cancer_stage_1['암T코드#10'].map(lambda x: x.lower())
cancer_stage_1['암N코드#11'] = cancer_stage_1['암N코드#11'].map(lambda x: x.lower())
cancer_stage_1['암M코드#12'] = cancer_stage_1['암M코드#12'].map(lambda x: x.lower())
# %%
def cancer_stage_from_TNM(T, N, M):
    expr_1= re.compile('[1]')
    expr_2 = re.compile('[2]')
    expr_3 = re.compile('[2]')
    expr_1_to_2 = re.compile('[1-2]')
    expr_1_to_3 = re.compile('[1-3]')
    if T == 'is' and N == '0' and M == '0':
        return 0
    elif expr_1_to_2.match(T) and N == '0' and M == '0':
        return 'Ⅰ'
    elif expr_1_to_2.match(T) and expr_1_to_3.match(N) and M == '0' :
        return 'ⅡA'
    elif expr_3.match(T) or T=='4a' and N == '0' and M ==' 0':
        return 'ⅡB'
    elif expr_3.match(T) or T=='4a' and expr_1_to_3.match(N) and M == '0':
        return 'Ⅲ'
    elif T == '4b' and M == '0':
        return 'ⅣA'
    elif expr_1.match(M):
        return 'ⅣB'
    else:
        None

# %%
cancer_stage_1['cancer_stage'] = cancer_stage_1.apply(lambda x: cancer_stage_from_TNM(x['암T코드#10'],
                                                                                      x['암N코드#11'],
                                                                                      x['암M코드#12']), axis=1)

# %%
cancer_stage_3['7th Surgical T#15'] = cancer_stage_3['7th Surgical T#15'].fillna(cancer_stage_3['8th Surgical   T#9'])
cancer_stage_3['7th Surgical N#16'] = cancer_stage_3['7th Surgical N#16'].fillna(cancer_stage_3['8th Surgical  N#10'])
cancer_stage_3['7th Surgical M#17'] = cancer_stage_3['7th Surgical M#17'].fillna(cancer_stage_3['8th Surgical  M#11'])
# %%
cancer_stage_3 = cancer_stage_3.dropna(subset=['7th Surgical T#15'])
cancer_stage_3 = cancer_stage_3.dropna(subset=['7th Surgical N#16'])
cancer_stage_3 = cancer_stage_3.dropna(subset=['7th Surgical M#17'])
cancer_stage_3['7th Surgical T#15'] = cancer_stage_3['7th Surgical T#15'].map(lambda x: x.lower())
cancer_stage_3['7th Surgical N#16'] = cancer_stage_3['7th Surgical N#16'].astype(int)
cancer_stage_3['7th Surgical M#17'] = cancer_stage_3['7th Surgical M#17'].astype(int)
# %%
cancer_stage_3['cancer_stage'] = cancer_stage_3.apply(lambda x: cancer_stage_from_TNM(x['7th Surgical T#15'],
                                                                                        str(x['7th Surgical N#16']),
                                                                                        str(x['7th Surgical M#17'])), axis=1)
# %%
cancer_stage_2['cancer_stage'] = cancer_stage_2['AJCC 7th:Stage#7'].fillna(cancer_stage_2['Stage(AJCC 7th)#11'])
cancer_stage_2['cancer_stage'] = cancer_stage_2['cancer_stage'].dropna()
cancer_stage_2['cancer_stage'] = cancer_stage_2['cancer_stage'].map(lambda x: x.split()[-1] if type(x) == str else x)
# %%
cancer_stage_1 = cancer_stage_1.dropna(subset=['cancer_stage'])
cancer_stage_2 = cancer_stage_2.dropna(subset=['cancer_stage'])
cancer_stage_3 = cancer_stage_3.dropna(subset=['cancer_stage'])
# %%
cancer_stage_1 = cancer_stage_1.drop_duplicates(subset=['환자번호#1'])[['환자번호#1', 'cancer_stage', '본원진단일자#4']]
cancer_stage_2 = cancer_stage_2.drop_duplicates(subset=['환자번호#1'])[['환자번호#1', 'cancer_stage', '진료일시#3']]
cancer_stage_3 = cancer_stage_3.drop_duplicates(subset=['환자번호#1'])[['환자번호#1', 'cancer_stage', '진료일시#4']]
cancer_stage_1.columns = ['환자번호#1', 'cancer_stage', 'cancer_stage_date']
cancer_stage_2.columns = ['환자번호#1', 'cancer_stage', 'cancer_stage_date']
cancer_stage_3.columns = ['환자번호#1', 'cancer_stage', 'cancer_stage_date']
# cancer_stage_1 = cancer_stage_1.drop_duplicates(subset=['환자번호#1'])[['환자번호#1', '본원진단일자#4']]
# cancer_stage_2 = cancer_stage_2.drop_duplicates(subset=['환자번호#1'])[['환자번호#1', '진료일시#3']]
# cancer_stage_3 = cancer_stage_3.drop_duplicates(subset=['환자번호#1'])[['환자번호#1', '진료일시#4']]
# cancer_stage_1.columns = ['환자번호#1', 'cancer_stage_date']
# cancer_stage_2.columns = ['환자번호#1', 'cancer_stage_date']
# cancer_stage_3.columns = ['환자번호#1', 'cancer_stage_date']
# %%
cancer_csv = pd.concat([cancer_stage_1, cancer_stage_2, cancer_stage_3])
cancer_csv = cancer_csv.drop_duplicates(subset=['환자번호#1'])

# %%
csv = pd.read_excel('../data_with_family_hx/data_any_bx.xlsx')
csv = pd.merge(csv, cancer_csv, how='left', left_on=['환자번호'], right_on=['환자번호#1']).drop(['환자번호#1'], axis=1)
csv['family_hx'] = csv['family_hx'].fillna('N')
# %%
csv['cancer_stage'] = csv.apply(lambda x: x['cancer_stage'] if str(x['cancer_date']) != "NaT" else None, axis=1)
csv['cancer_stage_date'] = csv.apply(lambda x: x['cancer_stage_date'] if str(x['cancer_date']) != "NaT" else None, axis=1)
# %%
csv['group'] = csv['group'].replace({3:1, 4:2})
# %%
# print(len(csv[(csv['cancer_stage_date'] - csv['index_date']).map(lambda x: x.days) < 0]))
# %%
# csv['cancer_stage_date'] = csv['cancer_stage_date'].fillna('2022-10-31')
# csv['cancer_stage_date'] = csv['cancer_stage_date'].map(lambda x: x if x < '2021-10-13' else None)

# # %%
# csv['cancer_stage_date'] = pd.to_datetime(csv['cancer_stage_date'])
# csv = csv[~((csv['cancer_stage_date'] - csv['index_date']).map(lambda x: x.days) < 0)]
# csv['cancer_not_from_stage'] = csv['cancer_date'].dropna().map(lambda x: 'Y')
# csv['cancer_date'] = csv['cancer_date'].fillna(csv['cancer_stage_date'])
# %%
csv.to_excel('../data_with_family_hx/data_any_bx.add_stage.xlsx', index=False)
# %%
csv = pd.read_csv('../data_with_family_hx/any_bx.cov.fillna_cancer.up_death.final_fu.add_fu.csv')
csv = pd.merge(csv, cancer_csv, how='left', left_on=['환자번호'], right_on=['환자번호#1']).drop(['환자번호#1'], axis=1)
# %%
csv['cancer_stage'] = csv.apply(lambda x: x['cancer_stage'] if type(x['cancer_date']) != float else None, axis=1)
csv['cancer_stage_date'] = csv.apply(lambda x: x['cancer_stage_date'] if type(x['cancer_date']) != float else None, axis=1)
# %%
# csv['cancer_stage_date'] = csv['cancer_stage_date'].fillna('2022-10-31')
# csv['cancer_stage_date'] = csv['cancer_stage_date'].map(lambda x: x if x < '2021-10-13' else None)
# csv['cancer_stage_date'] = pd.to_datetime(csv['cancer_stage_date'])
# csv['index_date'] = pd.to_datetime(csv['index_date'])
# csv = csv[~((csv['cancer_stage_date'] - csv['index_date']).map(lambda x: x.days) < 0)]
# %%
# def apply_fn(cancer_fu, cancer_fu_date, cancer_stage_date):
#     if cancer_fu == 'Y':
#         return cancer_fu_date
#     elif cancer_fu == 'N':
#         return cancer_stage_date
    
# csv['cancer_fu_date_with_stage'] = csv.dropna(subset=['cancer_stage_date']).apply(\
#                                                 lambda x: apply_fn(x['cancer_fu'],
#                                                                 x['cancer_fu_date'],
#                                                                 x['cancer_stage_date']), axis=1)
# csv['cancer_fu_date_with_stage'] = csv['cancer_fu_date_with_stage'].fillna(csv['cancer_fu_date'])
# csv['cancer_fu_with_stage'] = csv.dropna(subset=['cancer_stage_date']).apply(lambda x: 'Y' if x['cancer_fu'] == 'N' else x['cancer_fu'], axis=1)
# %%

csv.to_csv('../data_with_family_hx/any_bx.cov.fillna_cancer.up_death.final_fu.add_fu.cancer_stage.csv', index=False)
# %%
