# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tableone import TableOne
import warnings
from lifelines import CoxPHFitter
from lifelines import KaplanMeierFitter
from lifelines import NelsonAalenFitter
warnings.filterwarnings("ignore", category=DeprecationWarning) 
pd.set_option('display.max_columns', None)

# %%
csv = pd.read_csv('../data_for_analysis/any_bx.cov.fillna_cancer.up_death.final_fu.add_fu.csv')
# %%
csv['처방일자'] = pd.to_datetime(csv['처방일자'])
csv['final_fu_death'] = pd.to_datetime(csv['final_fu_death'])
csv['cancer_fu_date'] = pd.to_datetime(csv['cancer_fu_date'])
csv['first_fu'] = pd.to_datetime(csv['first_fu'])

# %%
csv['사망여부'] = csv['사망여부'].replace({'N':0, 'Y':1})
csv['사망여부'] = csv['사망여부'].fillna(0).astype(int)

naf = NelsonAalenFitter()
naf.fit(durations=csv.query('group == 1').apply(lambda x: x['cancer_fu_date'] - x['first_fu'], axis=1),
        event_observed=csv.query('group == 1')['group'], label='group_1')
naf.plot_cumulative_hazard()
naf.fit(durations=csv.query('group == 2').apply(lambda x: x['cancer_fu_date'] - x['first_fu'], axis=1),
        event_observed=csv.query('group == 2')['group'], label='group_2')
naf.plot_cumulative_hazard()
naf.fit(durations=csv.query('group == 3').apply(lambda x: x['cancer_fu_date'] - x['first_fu'], axis=1),
        event_observed=csv.query('group == 3')['group'], label='group_3')
naf.plot_cumulative_hazard()
naf.fit(durations=csv.query('group == 4').apply(lambda x: x['cancer_fu_date'] - x['first_fu'], axis=1),
        event_observed=csv.query('group == 4')['group'], label='group_4')
naf.plot_cumulative_hazard()
plt.xlabel("Days passed")
plt.ylabel("cumulative hazard of cancer")
plt.title("NelsonAalenFitter plot about cancer")
plt.legend(loc='upper left')
# %%
