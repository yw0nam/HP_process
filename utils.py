import pandas as pd
import re
import numpy as np

def map_fn(x):
    if type(x) == str:
        return x
    else:
        return 0

def find_positive(x):
    x = re.sub(r"\s+","", x)
    p = re.compile('(Result:)')
    text = x[p.search(x).end():].lower()
    text = re.sub(r"\W", "", text)
    if text == 'positive':
        return 1
    elif text == 'negative':
        return 0
    else:
        if 'positive' in text:
            return 1
        elif 'negative' in text:
            return 0
        else:
            return -1
    
def find_text(x, p):
    res = p.search(x)
    if res:
        return 1
    else:
        return 0
    
def find_index(data, p, return_csv=False):
    csv = data.copy()
    csv['검사결과내용#7_process'] = csv['검사결과내용#7_process'].map(lambda x: find_text(x.lower(), p))
    csv = csv[csv['검사결과내용#7_process'] != 0]
    if return_csv:
        return csv.index, csv
    else:
        return csv.index

def spilt_date(csv):
    csv_2001_2010 = csv[(csv['처방일자#3'] >= '2001-01-01') & (csv['처방일자#3'] <= '2010-12-31')]
    csv_2011_2016_06 = csv[(csv['처방일자#3'] >= '2011-01-01') & (csv['처방일자#3'] <= '2016-07-01')]
    csv_2016_06_2020 = csv[(csv['처방일자#3'] >= '2016-07-02') & (csv['처방일자#3'] <= '2020-12-31')]
    return csv_2001_2010, csv_2011_2016_06, csv_2016_06_2020