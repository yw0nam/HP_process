# %%
import argparse
from tqdm import tqdm
from utils import *
# from elasticsearch import Elasticsearch, helpers
import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
pd.set_option('display.max_columns', None)

def define_argparser():
    p = argparse.ArgumentParser()

    p.add_argument('--folder', required=True)
    p.add_argument('--dataset_name', required=True)
    config = p.parse_args()

    return config

# %%
config = define_argparser()
csv = pd.read_csv('../%s/apply_exclusion.csv'%config.folder)
# csv = csv.drop_duplicates('환자번호#1')
bert_predict = pd.read_csv('../data/analysis_bert_predict.csv', index_col=0)
csv_bert = csv.query('index in @bert_predict.index')
csv_date = csv.copy()
eradication_csv_1 = pd.read_csv("../data/HP_drug_1_unlock.csv", 
                              index_col=0, encoding='CP949')
eradication_csv_2 = pd.read_csv("../data/HP_drug_2_unlock.csv", 
                              index_col=0, encoding='CP949')
# %%
ids = """9AC558D65B79
04BDCD741155
1AFB512C82A3
3022C503FFF5
3FEBB3B96B55
A0B832BFF72D
C1D75C2111A9
E4FF02C660DF
F7A27A7295ED"""
ids = list(set(eradication_csv_1['환자번호#1'].to_list()  + eradication_csv_2['환자번호#1'].to_list())) + ids.split()
index_eradication = list(csv[csv['환자번호#1'].isin(ids)].index)

index_160 = list(csv[csv['TRT_HELICO_PYLORI#160'] == 1].index)
index_161 = list(csv[csv['STATUS_HELICO_PYLORI#161'].isin([1, 2])].index)
index = list(set(index_160+index_161 + index_eradication))
# %%
expr = 'index in @index'
data_1 = csv.query(expr)

temp = data_1[data_1['검사결과내용(최초1) #110'].map(lambda x: map_fn(x) != 0)]

bert_pred_1 = bert_predict.query('index in @temp.index')
temp['result'] = bert_pred_1
temp = temp.query('result == 0')
temp = temp[temp['검사명(최초1) #109'] != 'Urease Breath Test']

temp = temp.dropna(subset=['result'])
csv_bx_1 = temp[temp['검사명(최초1) #109'] != 'Urease Breath Test']

# %%
temp = data_1.copy()
temp = temp[temp['검사결과내용(최초1) #104'].map(lambda x: map_fn(x) != 0)]
p = re.compile('CLO.*[(]\s*[-]\s*[)]')
csv_clo = temp[temp['검사결과내용(최초1) #104'].map(lambda x: find_text(x, p)) == 1]

cz_index = list(set(list(csv_bx_1.index) + list(csv_clo.index)))
csv_cz_1 = data_1.query('index in @cz_index')

# %%
temp = data_1[data_1['검사결과내용(최초1) #116'].map(lambda x: map_fn(x) != 0)]
query_text = ['result[\s]*:[\s]*negative', 'result[\s]*:[\s]*neagtive',
             'result[\s]*:[\s]*negaitve', 'result[\s]*:[\s]*negatie']
p = re.compile('|'.join(query_text))
csv_ubt_1 = temp[temp['검사결과내용(최초1) #116'].map(lambda x: find_text(x.lower(), p)) == 1]

#%%
temp = data_1[data_1['검사결과내용(최초1) #110'].map(lambda x: map_fn(x) != 0)]
query_text = ['result[\s]*:[\s]*negative', 'result[\s]*:[\s]*neagtive',
             'result[\s]*:[\s]*negaitve', 'result[\s]*:[\s]*negatie']
p = re.compile('|'.join(query_text))
csv_ubt_df_1 = temp[temp['검사결과내용(최초1) #110'].map(lambda x: find_text(x.lower(), p)) == 1]
# %%
csv_date['Group_1_DL'] = csv_ubt_1['처방일자(최초1) #113']
csv_date['Group_1_CZ'] = csv_cz_1['처방일자(최초1) #101']
csv_date['Group_1_DF'] = csv_ubt_df_1['처방일자(최초1) #107']

group_1 = list(set(list(csv_ubt_1.index) + list(csv_ubt_df_1.index)+ list(csv_cz_1.index)))

# %% 
## Group 2 After Eradication (+)
temp = data_1.copy()
temp = temp[temp['검사결과내용(최초1) #104'].map(lambda x: map_fn(x)) != 0]
p = re.compile('CLO.*[(]\s*[+]\s*[)]')
temp = temp[temp['검사결과내용(최초1) #104'].map(lambda x: find_text(x, p)) == 1]

exclude_index = [9774, 79298, 100266]

expr = 'index not in @exclude_index'
csv_clo_2 = temp.query(expr)
# %%
temp = data_1[data_1['검사결과내용(최초1) #116'] != '']
temp = temp[temp['검사결과내용(최초1) #116'].map(lambda x: map_fn(x)) != 0]
p = re.compile('result[\s]*:[\s]*positive')
csv_ubt_2 = temp[temp['검사결과내용(최초1) #116'].map(lambda x: find_text(x.lower(), p)) == 1]
# %%
temp = data_1[data_1['검사결과내용(최초1) #110'] != '']
temp = temp[temp['검사결과내용(최초1) #110'].map(lambda x: map_fn(x)) != 0]
temp = temp[temp['검사명(최초1) #109'] == 'Urease Breath Test']

p = re.compile('result[\s]*:[\s]*positive')
csv_ubt_2_df = temp[temp['검사결과내용(최초1) #110'].map(lambda x: find_text(x.lower(), p)) == 1]
# %%
temp = data_1[data_1['검사결과내용(최초1) #110'].map(lambda x: map_fn(x) != 0)]

bert_pred_2 = bert_predict.query('index in @temp.index')
temp['result'] = bert_pred_2
data_hp_plus_2 = temp.query('result == 1')
data_hp_plus_2 = data_hp_plus_2[data_hp_plus_2['검사명(최초1) #109'] != 'Urease Breath Test']
cz_index = list(set(list(data_hp_plus_2.index) + list(csv_ubt_2_df.index)))
csv_cz_2 = data_1.query('index in @cz_index')
# %%
csv_date['Group_2_DL'] = csv_ubt_2['처방일자(최초1) #113']
csv_date['Group_2_CZ'] = csv_clo_2['처방일자(최초1) #101']
csv_date['Group_2_DF'] = csv_cz_2['처방일자(최초1) #107']
group_2 = list(set(list(csv_ubt_2.index) + list(csv_clo_2.index)+ list(csv_cz_2.index)))

# %% 
## Group 3 Not Eradication (+)
data_3 = csv.query('index not in @index')
temp = data_3[data_3['검사결과내용(최초1) #104'] != '']
temp = temp[temp['검사결과내용(최초1) #104'].map(lambda x: map_fn(x)) != 0]
p = re.compile('CLO.*[(]\s*[+]\s*[)]')
temp = temp[temp['검사결과내용(최초1) #104'].map(lambda x: find_text(x, p)) == 1]
exclude_index = [9774, 79298, 100266]

expr = 'index not in @exclude_index'
csv_clo_3 = temp.query(expr)

# %%
temp = data_3[data_3['검사결과내용(최초1) #116'] != '']
temp = temp[temp['검사결과내용(최초1) #116'].map(lambda x: map_fn(x)) != 0]
p = re.compile('result[\s]*:[\s]*positive')
csv_ubt_3 = temp[temp['검사결과내용(최초1) #116'].map(lambda x: find_text(x.lower(), p)) == 1]
# %%
temp = data_3[data_3['검사결과내용(최초1) #110'] != '']
temp = temp[temp['검사결과내용(최초1) #110'].map(lambda x: map_fn(x)) != 0]
temp = temp[temp['검사명(최초1) #109'] == 'Urease Breath Test']

p = re.compile('result[\s]*:[\s]*positive')
csv_ubt_3_df = temp[temp['검사결과내용(최초1) #110'].map(lambda x: find_text(x.lower(), p)) == 1]
# %%
temp = data_3[data_3['검사결과내용(최초1) #110'].map(lambda x: map_fn(x) != 0)]

bert_pred_3 = bert_predict.query('index in @temp.index')
temp['result'] = bert_pred_3
data_hp_plus_3 = temp.query('result == 1')
data_hp_plus_3 = data_hp_plus_3[data_hp_plus_3['검사명(최초1) #109'] != 'Urease Breath Test']
cz_index_3 = list(set(list(data_hp_plus_3.index) + list(csv_ubt_3_df.index)))
csv_cz_3 = data_3.query('index in @cz_index_3')
# %%
csv_date['Group_3_DL'] = csv_ubt_3['처방일자(최초1) #113']
csv_date['Group_3_CZ'] = csv_clo_3['처방일자(최초1) #101']
csv_date['Group_3_DF'] = csv_cz_3['처방일자(최초1) #107']
group_3 = list(set(list(csv_ubt_3.index) + list(csv_clo_3.index)+ list(csv_cz_3.index)))
# %%
## Group 4 Not Eradication (-)
temp = data_3[data_3['검사결과내용(최초1) #110'].map(lambda x: map_fn(x) != 0)]

bert_pred_4 = bert_predict.query('index in @temp.index')
temp['result'] = bert_pred_4
temp = temp.query('result == 0')
temp = temp.dropna(subset=['result'])
csv_bx_4 = temp[temp['검사명(최초1) #109'] != 'Urease Breath Test']
# %%
temp = data_3.copy()
temp = temp[temp['검사결과내용(최초1) #104'].map(lambda x: map_fn(x) != 0)]
p = re.compile('CLO.*[(]\s*[-]\s*[)]')
csv_clo_4 = temp[temp['검사결과내용(최초1) #104'].map(lambda x: find_text(x, p)) == 1]
cz_index = list(set(list(csv_bx_4.index) + list(csv_clo_4.index)))
csv_cz_4 = data_3.query('index in @cz_index')
# %%
temp = data_3[data_3['검사결과내용(최초1) #116'].map(lambda x: map_fn(x) != 0)]

query_text = ['result[\s]*:[\s]*negative', 'result[\s]*:[\s]*neagtive',
             'result[\s]*:[\s]*negaitve', 'result[\s]*:[\s]*negatie']
p = re.compile('|'.join(query_text))
csv_ubt_4 = temp[temp['검사결과내용(최초1) #116'].map(lambda x: find_text(x.lower(), p)) == 1]
# %%
temp = data_3[data_3['검사결과내용(최초1) #110'].map(lambda x: map_fn(x) != 0)]

query_text = ['result[\s]*:[\s]*negative', 'result[\s]*:[\s]*neagtive',
             'result[\s]*:[\s]*negaitve', 'result[\s]*:[\s]*negatie']
p = re.compile('|'.join(query_text))
csv_ubt_df_4 = temp[temp['검사결과내용(최초1) #110'].map(lambda x: find_text(x.lower(), p)) == 1]
# %%
csv_date['Group_4_DL'] = csv_ubt_4['처방일자(최초1) #113']
csv_date['Group_4_CZ'] = csv_cz_4['처방일자(최초1) #101']
csv_date['Group_4_DF'] = csv_ubt_df_4['처방일자(최초1) #107']
group_4 = list(set(list(csv_ubt_4.index) + list(csv_clo_4.index)+ list(csv_cz_4.index)))
# %%
cols = list(csv_date.columns[173:])
valid_ls = []
# for i in tqdm(range(len(csv_date))):
for i in range(len(csv_date)):
    flag = 1
    for col in cols:
        if type(csv_date.iloc[i][col]) == str:
            valid_ls.append(1)
            flag = 0
            break
        else:
            continue
    if flag:
        valid_ls.append(0)
csv_date['valid'] = valid_ls
valid_data = csv_date.query('valid == 1')
# %%
group_1_col = cols[:3]
group_2_col = cols[3:6]
group_3_col = cols[6:9]
group_4_col = cols[9:12]

last_fu = []
first_fu = []
last_fu_name = []
first_fu_name = []

# for i in tqdm(range(len(valid_data))):
for i in range(len(valid_data)):
    col_name = []
    dates = []
    for col in cols:
        if type(valid_data.iloc[i][col]) == str:
            dates.append(valid_data.iloc[i][col])
            col_name.append(col)
    last_fu_idx, first_fu_idx = dates.index(max(dates)), dates.index(min(dates))
    
    last_fu.append(dates[last_fu_idx])
    last_fu_name.append(col_name[last_fu_idx])
    
    first_fu.append(dates[first_fu_idx])
    first_fu_name.append(col_name[first_fu_idx])
# %%
valid_data['last_fu'] = last_fu
valid_data['first_fu'] = first_fu
valid_data['last_fu_name'] = last_fu_name
valid_data['first_fu_name'] = first_fu_name

group_1_df = valid_data.query('last_fu_name in @group_1_col')
group_2_df = valid_data.query('last_fu_name in @group_2_col')
group_3_df = valid_data.query('last_fu_name in @group_3_col')
group_4_df = valid_data.query('last_fu_name in @group_4_col')

group_1_df['group'] = 1
group_2_df['group'] = 2
group_3_df['group'] = 3
group_4_df['group'] = 4

valid_data = pd.concat([group_1_df, group_2_df, group_3_df, group_4_df])
# %%
col_ls = group_1_col + group_4_col
# %%
first_fu = []
first_fu_name = []
# for i in tqdm(range(len(valid_data))):
for i in range(len(valid_data)):
    col_name = []
    dates = []
    for col in col_ls:
        if type(valid_data.iloc[i][col]) == str:
            dates.append(valid_data.iloc[i][col])
            col_name.append(col)
    if dates == []:
        first_fu.append(None)
        first_fu_name.append(None)
        continue
    else:
        first_fu_idx = dates.index(min(dates))
        first_fu.append(dates[first_fu_idx])
        first_fu_name.append(col_name[first_fu_idx])

valid_data['first_negative_date'] = first_fu
valid_data['first_negative_name'] = first_fu_name

# %%
fu_date_list = []
fu_name_list = []
# for i in tqdm(range(len(valid_data))):
for i in range(len(valid_data)):
    col_name = []
    dates = []
    for col in cols:
        if type(valid_data.iloc[i][col]) == str:
            dates.append(valid_data.iloc[i][col])
            col_name.append(col)
    fu_date_list.append('|'.join(dates))
    fu_name_list.append('|'.join(col_name))

valid_data['fu_dates'] = fu_date_list
valid_data['fu_names'] = fu_name_list
# %%
valid_data.to_csv('../%s/%s.csv'%(config.folder, config.dataset_name), index=False)

# %%
