# %%
import re
import numpy as np
import datatable
import pandas as pd
pd.set_option('display.max_columns', None)
# %%
csv = datatable.fread('./data_2/HP_2011_20160701.csv').to_pandas()
csv.head()
# %%
def map_fn(x):
    if type(x) == str:
        return x
    else:
        return 0

def find_text(x):
    x = re.sub(r"\s+","", x)
    p = re.compile('(Result:)')
    text = x[p.search(x).end():].lower()
    if text == 'positive':
        return 1
    elif text == 'negative':
        return 0
    else:
        return -1

# %%
csv['검사결과내용#15'].value_counts()
# %%

# 검사결과내용#15 (HP 진단문 -> HP유무 판정)
csv['검사결과내용#15_process'] = csv['검사결과내용#15'].map(lambda x: map_fn(x))
csv_15 = csv[csv['검사결과내용#15_process'] != '']
csv_15 = csv_15[csv_15['검사결과내용#15_process'] != 0]
# %%
csv_15_bert = pd.read_csv('./data_2/HP_2011_20160701_predict.csv', index_col=0)
csv_15['result'] = csv_15_bert
csv_15 = csv_15[csv_15['result'] == 1]
csv_15

# %%
csv['검사결과내용#20'].value_counts()
# %%
# 검사결과내용#20에서 positive인 경우만 추출
csv['검사결과내용#20_process'] = csv['검사결과내용#20'].map(lambda x: map_fn(x))
csv_20 = csv[csv['검사결과내용#20_process'] != '']
csv_20 = csv_20[csv_20['검사결과내용#20_process'] != 0]
csv_20['result'] = csv_20['검사결과내용#20'].map(lambda x: find_text(x))
csv_20 = csv_20[csv_20['result'] == 1]

# %%
csv_24 = csv[csv['건강검진결과코드#24'] == 'G020']
csv_24
# %%

# 사용데이터만 추출
index = list(set(list(csv_20.index)) | set(list(csv_15.index)) | set(list(csv_24.index)) )
data = csv[csv.index.isin(index)]
data
# %%
#제외기준 2 위수술이력 문진 == 1
print(data[data['SURGERY_STOMACH#138'] != 1].value_counts())
data = data[data['SURGERY_STOMACH#138'] != 1]
data
# %%
#제외기준 3 가족중 위장암존재
data = data[data['FAMILY_CANCER_STOMACH_F'] != 1]
data = data[data['FAMILY_CANCER_STOMACH_M'] != 1]
data = data[data['FAMILY_CANCER_STOMACH_SIB'] != 1]
data = data[data['FAMILY_CANCER_STOMACH_CH'] != 1]