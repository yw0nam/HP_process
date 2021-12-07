# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tableone import TableOne
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
pd.set_option('display.max_columns', None)
# %%
csv = pd.read_csv('../data_for_analysis/bx_for_hp.cov.fillna_cancer.up_death.final_fu.add_fu.csv')
# %%
csv['사망여부'] = csv['사망여부'].replace({'N':0, 'Y':1})
csv['사망여부'] = csv['사망여부'].fillna(0).astype(int)
csv['cancer_fu'] = csv['cancer_fu'].replace({'N':0, 'Y':1})
csv['cancer_fu'] = csv['cancer_fu'].fillna(0).astype(int)
# %%
csv['처방일자'] = pd.to_datetime(csv['처방일자'])
csv['final_fu_death'] = pd.to_datetime(csv['final_fu_death'])
csv['cancer_fu_date'] = pd.to_datetime(csv['cancer_fu_date'])
csv['first_fu'] = pd.to_datetime(csv['first_fu'])
csv['index_date'] = pd.to_datetime(csv['index_date'])
# %%
csv['group'] = csv['group'].replace({3:1, 4:2})
csv['cancer_fu_duration'] = (csv['cancer_fu_date'] - csv['index_date']).map(lambda x: x.days)
csv['death_fu_duration'] = (csv['final_fu_death'] - csv['index_date']).map(lambda x: x.days) 
csv = csv.drop('cancer', axis=1)
csv = csv.rename({'사망여부':'death', 'cancer_fu':'cancer'}, axis=1)
# %%
cols = ['age', 'BMI', 'CCI', 'Hb', 'TG', 
                'HDL', 'LDL', 'glucose',
                'sex', 'smoking', 'alcohol_drinking', 
                'physical_activity', 'EGD', 'cancer', 
                'death', 'death_fu_duration', 'cancer_fu_duration']

category_cols = ['sex', 'smoking', 'alcohol_drinking', 
                'physical_activity', 'EGD', 'cancer', 'death']

mytable = TableOne(csv, columns=cols, categorical=category_cols,
                   groupby='group', pval=True, nonnormal='bili')
print(mytable.tabulate(tablefmt="rst"))

# %%
mytable = TableOne(csv.query("group == 2").query("cancer == 1"), columns=cols, categorical=category_cols,
                nonnormal='bili')
print(mytable.tabulate(tablefmt="rst"))
# %%
