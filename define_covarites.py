# %%
import pandas as pd
import numpy as np
import re
pd.set_option('display.max_columns', None)

# %%
csv = pd.read_csv('./data/grouping_data.csv')
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
death = pd.read_csv('./data/die.csv', index_col=0)
csv_add_death = pd.merge(csv, death, how='left', 
                left_on=['환자번호'], 
                right_on=['환자번호'])
cols = list(valid.columns[-7:])
data = pd.concat([csv_add_death, valid[cols]], axis=1)

data.to_csv('./data_for_analysis/hp_bx.csv')
data.to_excel('./data_for_analysis/hp_bx.xlsx')