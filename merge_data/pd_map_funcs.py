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

def smoke_map_fn(x):
    if type(x) != str:
        return None
    elif x[0] == '①':
        return 0
    elif x[0] == '②':
        return 1
    elif x[0] == '③':
        return 2