# %%
import pandas as pd
import numpy as np
import re
pd.set_option('display.max_columns', None)

# %%
csv = pd.read_csv('./data_for_analysis/bx_for_hp.csv')
valid = csv[csv['valid'] == 1]
# %%
csv = valid[['환자번호#1', '처방일자#3']]
csv.columns = ['환자번호', '처방일자']
csv['age'] = valid['처방일자{연령}#4']
# %%
csv['sex'] = valid['성별#8']

def map_fn(x):
    if x == 'M':
        return 1
    elif x == 'F':
        return 0
    
csv['sex'] = csv['sex'].map(lambda x: map_fn(x))
# %%
csv['BMI'] = valid['검사결과수치값#48']
csv['smoking'] = valid['SMK#130']
# %%
csv['alcohol_drinking'] = valid['ALC_AMOUNT_GRAMS#134']
csv['alcohol_drinking'] = csv['alcohol_drinking'].fillna(0)

def map_fn(x):
    if x == 0:
        return 0
    elif x <= 10:
        return 1
    elif x > 10:
        return 2

csv['alcohol_drinking'] = csv['alcohol_drinking'].map(lambda x: map_fn(x))
# %%
def apply_fn(phy_136, phy_137):
    if phy_136 in [0, 1] or phy_137 in [0, 1]:
        return 0
    elif phy_136 in [2, 3, 4] or phy_137 in [2, 3]:
        return 1
    else:
        return None
csv['physical_activity'] = valid.apply(lambda x: apply_fn(x['PHY_FREQ_2009#136'], 
                                                          x['PHY_FREQ#137']), axis='columns')
# %%
def apply_fn(dicts):
    result = 0
    result += cal_age(dicts['처방일자{연령}#4'])
    if dicts['HISTORY_MI#147'] == 1:
        result += 1
    result += cal_pvd(dicts['검사결과수치값#98'])
    if dicts['HISTORY_STROKE#139'] == 1:
        result += 1
    if dicts['HISTORY_COPD#146'] == 1:
        result += 1
    if dicts['HISTORY_GA_DUODENAL_ULCER#140'] == 1:
        result += 1
    if dicts['HISTORY_FATTY_LIVER#141'] == 1 or dicts['HISTORY_HBV#143'] == 1 or dicts['HISTORY_HCV#144'] == 1:
        result += 1
    elif dicts['HISTORY_HEP_CIRRHOSIS#142'] == 1 or dicts['HISTORY_CIRRHOSIS#145']:
        result += 3
    if dicts['HISTORY_DIABETES#156'] == 1 or dicts['TRT_DIABETES#157'] == 1:
        result += 1
    if dicts['검사결과수치값#63'] < 60:
        result += 2
    if dicts['HISTORY_CANCER#149'] == 1:
        result += 2
    if dicts['검사결과수치값#88'] == 'POSITIVE':
        result += 6
    return result
        
def cal_age(age):
    if age >= 50 and age <= 59:
        return 1
    elif age >= 60 and age <= 69:
        return 3
    elif age >= 80:
        return 4
    else:
        return 0
    
def cal_pvd(pvd):
    if type(pvd) != str:
        return 0
    else:
        split_txt = pvd.split('/')
        for txt in split_txt:
            if float(txt) < 0.9 or float(txt) > 1.4:
                return 1
        return 0
csv['CCI'] = valid.apply(lambda x: apply_fn(x.to_dict()), axis=1)

csv['Hb'] = valid['검사결과수치값#53']
csv['TG'] = valid['검사결과수치값#73']
csv['BZ'] = valid['검사결과수치값#78']
csv['LDL'] = valid['검사결과수치값#83']
csv['glucose'] = valid['검사결과수치값#58']
# %%
def map_fn(x):
    find_txts = ['chro\w+\s*atro\w*\s*gast\w*\s*', 'metapl\w+\s*gast\w+\s*', 
                 'lymphofolli\w+\s*gastr\w+\s*', 'chro\w+\s*super\w+\s*gastr\w+\s*']
    names = ['CAG', 'MG', 'LFG', 'CSG']
    for i in range(len(names)):
        exp = re.compile(find_txts[i])
        res = exp.search(x)
        if res != None:
            return names[i]
    return 'WNL'
csv['EGD'] = valid['검사결과내용#7'].map(lambda x: map_fn(x.lower()))
# %%

def map_fn(x):
    find_txts = ['adeno\w+\shig\w+\sgra\w+\sdyspla\w+\s', 'adeno\w+\s']
    names = [2, 1]
    for i in range(len(names)):
        
        exp = re.compile(find_txts[i])
        if type(x) != str:
            return None
        res = exp.search(x)
        if res != None:
            return names[i]
    return 0
csv['Adenoma'] = valid['검사결과내용#15'].map(lambda x: map_fn(x))
# %%
cdw_df = pd.read_excel('./data/건진 사망자 데이터 확인.xlsx', sheet_name='CDW건진이력기준')
hab_df = pd.read_excel('./data/건진 사망자 데이터 확인.xlsx', sheet_name='행안부데이터기준')

cdw_df_filtered = cdw_df[['환자번호#1', '사망일자#20', '사망여부#19','사망원인코드#22', '사망원인명#23']]
hab_df_filtered = hab_df[['환자번호#1','사망일#2', '사망여부#11', '사망원인코드#14', '사망원인명#15']]

cdw_df_filtered.columns = ['환자번호', '사망일', '사망여부_', '사망원인코드_', '사망원인명_']
hab_df_filtered.columns = ['환자번호', '사망일', '사망여부_', '사망원인코드_', '사망원인명_']

hab_df_filtered = hab_df_filtered.query("사망여부_ == 'Y'")

death = pd.concat([cdw_df_filtered, hab_df_filtered], axis=0, ignore_index=True)
death = death.drop_duplicates(subset=['환자번호'])

die = pd.read_csv('./data/apply_exclusion.csv')
die['사망여부'] = die['사망일#10'].map(lambda x: 'Y' if type(x) != float else 'N')
die = die[['환자번호#1', '사망일#10', '사망여부']]
die = die[die['사망여부'] == 'Y']
die.columns = ['환자번호', '사망일', '사망여부_']

die = pd.concat([death, die])
die.columns = ['환자번호', '사망일', '사망여부', '사망원인코드', '사망원인명']
# %%

csv = pd.merge(csv, die, how='left',
        left_on=['환자번호'], right_on=['환자번호'])
csv = csv.drop_duplicates(subset='환자번호')
# %%
cols = list(valid.columns[-9:]) + ['환자번호#1']
data = pd.merge(csv, valid[cols], how='left',
                left_on=['환자번호'], right_on=['환자번호#1'])
# %%
data = data.drop(['환자번호#1'], axis=1)
# %%
data.to_csv('./data_for_analysis/bx_for_hp.cov.csv', index=False)
# %%

pd.read_csv('./data_for_analysis/bx_for_hp.cov.csv')
# %%
