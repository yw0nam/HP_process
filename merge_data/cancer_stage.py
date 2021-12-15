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
cancer_stage_1 = cancer_stage_1.drop_duplicates(subset=['환자번호#1'])[['환자번호#1', 'cancer_stage']]
cancer_stage_2 = cancer_stage_2.drop_duplicates(subset=['환자번호#1'])[['환자번호#1', 'cancer_stage']]
cancer_stage_3 = cancer_stage_3.drop_duplicates(subset=['환자번호#1'])[['환자번호#1', 'cancer_stage']]
# %%
cancer_csv = pd.concat([cancer_stage_1, cancer_stage_2, cancer_stage_3])
cancer_csv = cancer_csv.drop_duplicates(subset=['환자번호#1'])

# %%
csv = pd.read_excel('../data_with_family_hx/data_any_bx.xlsx')
csv = pd.merge(csv, cancer_csv, how='left', left_on=['환자번호'], right_on=['환자번호#1']).drop(['환자번호#1'], axis=1)
# %%
csv['family_hx'] = csv['family_hx'].fillna('N')
# %%
csv.to_excel('../data_with_family_hx/data_any_bx.xlsx', index=False)
# %%
