# %%
import numpy as np
import pandas as pd
from utils import *
pd.set_option('display.max_columns', None)

# %%
parser = csv_parser('./data_for_analysis/any_bx.csv')
parser.read_csv()
# %%
csv = parser.check_cancer(risk_path='./etc_data/건진 CANCER 관리 대상자-위암.xlsx',
                         bx_path='./etc_data/hp_stomach_cancer.csv',
                        histology_path='./data/apply_exclusion.csv')
# %%
csv = fill_bmi(csv, bmi_csv_path='./etc_data/HP-bmi.csv')
csv = fill_smoking(csv, smoke_csv_path='./etc_data/HP-smoking-missing.csv')
# %%
if 'Unnamed: 0' in csv.columns:
    csv = csv.drop('Unnamed: 0', axis='columns')
csv = csv.drop('환자번호#1', axis='columns')
csv = csv.drop_duplicates(subset='환자번호')
# %%

csv.to_csv('./data_for_analysis/any_bx_2021_10_25.csv', index=False)
# %%
import pandas as pd
# %%
csv = pd.read_csv('./data_for_analysis/hp_bx_2021_10_25.csv')
csv.to_excel('./data_for_analysis/hp_bx_cancer.xlsx', index=False)
# %%
