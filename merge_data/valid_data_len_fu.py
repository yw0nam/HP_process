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
csv = pd.read_csv('../data_for_analysis/any_bx.cov.fillna_cancer.up_death.final_fu.csv')
csv['처방일자'] = pd.to_datetime(csv['처방일자'])
csv['first_fu'] = pd.to_datetime(csv['first_fu'])
csv['last_fu'] = pd.to_datetime(csv['last_fu'])
csv['final_fu_cdw'] = pd.to_datetime(csv['final_fu_cdw'])

# %%
csv['fu_1to2'] = (csv['first_fu'] - csv['처방일자']).map(lambda x: x.days)
csv['final_fu_cdw'] = csv.apply(lambda x: None if (x['first_fu'] - x['final_fu_cdw']).days > 0 else x['final_fu_cdw'], axis=1)
# %%
# Make Final Death, Cancer Follow up
csv = csv.query('(fu_1to2 >= 180) and (fu_1to2 <= 1825)')
csv['final_fu_cdw'] = csv['final_fu_cdw'].fillna('K')
csv['temp'] = csv['fu_dates'] + '|' +  csv['final_fu_cdw'].astype(str)
csv['temp'] = csv['temp'].map(lambda x: x.split('|')[:-1] if x.split('|')[-1] == 'K' else x.split('|'))

# %%
csv = csv[csv['temp'].map(lambda x: len(list(set(x))) >= 2)]
 # %%
csv['final_fu_death'] = csv['사망일']
csv['final_fu_death'] = csv['final_fu_death'].fillna(csv['temp'].map(lambda x: max(x)))
csv = csv.drop(['temp', 'final_fu_cdw'], axis=1)
# %%
# csv['final_cancer_fu_date'] = csv['cancer_date']
csv['cancer_fu'] = csv.apply(lambda x: None if x['cancer'] == 'Y' and x['cancer_date'] >= '2021-10-12' else x['cancer'], axis=1)
csv['cancer_fu_date'] = csv['cancer_date'].fillna(csv['final_fu_death']).map(lambda x: '2021-10-12' if x >= '2021-10-12' else x)

# %%
csv['cancer_fu_date'] = pd.to_datetime(csv['cancer_fu_date'])
csv['final_fu_death'] = pd.to_datetime(csv['final_fu_death'])
# %%
def check_cancer_or_death(fu, fu_date, first_fu, fu_lenghth=1825):
    """[summary]

    Args:
        fu ([type]): Column that cancer or death
        fu_date ([type]): Column that cancer or death date
        first_fu ([type]): Column that First fu date
        fu_lenghth (int): fu length, Defaults to 1895.

    Returns:
        [type]: [description]
    """
    if fu != 'Y':
        return None
    else:
        if (fu_date - first_fu).days >= fu_lenghth:
            return 'Y'
        else:
            return 'N'
# %%
print(len(csv) - len(csv[csv.apply(lambda x: check_cancer_or_death(x['cancer_fu'],
                                              x['cancer_fu_date'],x['처방일자']), axis=1) != 'N']))
print(len(csv) - len(csv[csv.apply(lambda x: check_cancer_or_death(x['사망여부'],
                                              x['final_fu_death'],x['처방일자']), axis=1) != 'N']))
# %%
csv = csv[csv.apply(lambda x: check_cancer_or_death(x['cancer_fu'],
                                              x['cancer_fu_date'],x['처방일자']), axis=1) != 'N']
csv = csv[csv.apply(lambda x: check_cancer_or_death(x['사망여부'],
                                              x['final_fu_death'],x['처방일자']), axis=1) != 'N']
# %%
csv = csv.rename({'BZ':'HDL'}, axis=1) 
csv['사망여부'] =csv['사망여부'].fillna('N')
csv['cancer_fu'] =csv['cancer_fu'].fillna('N')
cols = ['age', 'BMI', 'CCI', 'Hb', 'TG', 
                'HDL', 'LDL', 'glucose',
                'sex', 'smoking', 'alcohol_drinking', 
                'physical_activity', 'EGD', 'Adenoma', 'cancer_fu', '사망여부']

category_cols = ['sex', 'smoking', 'alcohol_drinking', 
                'physical_activity', 'EGD', 'Adenoma'
                 , 'cancer_fu', '사망여부']

mytable = TableOne(csv, columns=cols, categorical=category_cols,
                   groupby='group', pval=True, nonnormal='bili')
print(mytable.tabulate(tablefmt="rst"))
# %%
csv.to_csv('./../data_for_analysis/bx_for_hp.cov.fillna_cancer.up_death.final_fu.add_fu.csv', index=False)
# %%
