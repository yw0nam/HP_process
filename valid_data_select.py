# %%
from utils import *
import re
import numpy as np
import pandas as pd
import datatable
pd.set_option('display.max_columns', None)
# %%
csv = datatable.fread('./data/concated.csv').to_pandas()
csv = csv.drop('C0', axis=1)
# %%

# 검사결과내용#15 (HP 진단문 -> HP유무 판정)
csv_15 = csv[csv['검사결과내용#15'] != '']
csv_15['result_text'] = csv_15['검사결과내용#15'].map(lambda x: map_fn(x))
csv_15 = csv_15[csv_15['result_text'] != 0]
# %%

bert_pred = pd.read_csv('./data/concat_pred.csv', index_col=0)
if len(csv_15) == len(bert_pred):
    csv_15['predict'] = bert_pred['prediction']
    csv_15_bert = csv_15[csv_15['predict'] == 1]
else:
    print('something wrong')
# csv_15
# %%
p = re.compile('infection')
csv_15_infect = csv_15[csv_15['검사결과내용#15'].map(lambda x: find_text(x, p)) != 0]
# %%
# 검사결과내용#20에서 positive인 경우만 추출
csv['검사결과내용#20_process'] = csv['검사결과내용#20'].map(lambda x: map_fn(x))
csv_20 = csv[csv['검사결과내용#20_process'] != '']
csv_20 = csv_20[csv_20['검사결과내용#20_process'] != 0]
csv_20['result'] = csv_20['검사결과내용#20'].map(lambda x: find_positive(x))
csv_20 = csv_20[csv_20['result'] == 1] # positive -> 1 negative -> 0
# csv_20
# %%
csv_24 = csv[csv['건강검진결과코드#24'] == 'G020']
# csv_24
# %%
csv_7 = csv[csv['검사결과내용#7'].map(lambda x: map_fn(x)) != 0]
csv_7 = csv_7[csv_7['검사결과내용#7'] != '']
p = re.compile('CLO.*[(]\s*[+]\s*[)]')
csv_7 = csv_7[csv_7['검사결과내용#7'].map(lambda x: find_text(x, p)) != 0]
# %%
# 사용데이터만 추출
index = list(set(list(csv_20.index)) | set(list(csv_15_infect.index)) | set(list(csv_24.index)) | set(list(csv_7.index)) | set(list(csv_15_bert.index)))
data = csv[csv.index.isin(index)]

# %%
data.to_csv('./data/include_criteria.csv')