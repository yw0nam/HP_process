# %%
import pandas as pd
from lifelines import CoxPHFitter
from lifelines import KaplanMeierFitter
from lifelines import NelsonAalenFitter
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('display.max_columns', None)
# %%

#csv = pd.read_csv('./data_for_analysis/hp_bx.fu365.fu_cdw.csv')
csv = pd.read_csv('./data_for_analysis/any_bx.fu_1_2_365.fu_cdw.exam_count.csv')
csv['사망여부'] = csv['사망여부'].replace({'N':0, 'Y':1})
csv['사망여부'] = csv['사망여부'].fillna(0).astype(int)
kmf = KaplanMeierFitter() 


group_1 = csv.query('group == 1')[['group', '사망여부','fu_days', 'cancer']]
group_2 = csv.query('group == 2')[['group', '사망여부', 'fu_days', 'cancer']]
group_3 = csv.query('group == 3')[['group', '사망여부', 'fu_days', 'cancer']]
group_4 = csv.query('group == 4')[['group', '사망여부', 'fu_days', 'cancer']]

# kmf.fit(durations=group_1['fu_days'], event_observed=group_1['cancer'], label='group_1')
# kmf.plot_cumulative_density()
# kmf.fit(durations=group_2['fu_days'], event_observed=group_2['cancer'], label='group_2')
# kmf.plot_cumulative_density()
# kmf.fit(durations=group_3['fu_days'], event_observed=group_3['cancer'], label='group_3')
# kmf.plot_cumulative_density()
# kmf.fit(durations=group_4['fu_days'], event_observed=group_4['cancer'], label='group_4')
# kmf.plot_cumulative_density()

naf = NelsonAalenFitter()
naf.fit(durations=group_1['fu_days'], event_observed=group_1['cancer'], label='group_1')
naf.plot_cumulative_hazard()
naf.fit(durations=group_2['fu_days'], event_observed=group_2['cancer'], label='group_2')
naf.plot_cumulative_hazard()
naf.fit(durations=group_3['fu_days'], event_observed=group_3['cancer'], label='group_3')
naf.plot_cumulative_hazard()
naf.fit(durations=group_4['fu_days'], event_observed=group_4['cancer'], label='group_4')
naf.plot_cumulative_hazard()
plt.ylim(0, 0.6)
plt.xlabel("Days passed")
plt.ylabel("cumulative hazard of cancer")
plt.title("NelsonAalenFitter plot about cancer")
plt.legend(loc='upper left')
# %%

kmf.fit(durations=group_1['fu_days'], event_observed=group_1['사망여부'], label='group_1')
kmf.plot_survival_function()
kmf.fit(durations=group_2['fu_days'], event_observed=group_2['사망여부'], label='group_2 and 3')
kmf.plot_survival_function()
kmf.fit(durations=group_3['fu_days'], event_observed=group_3['사망여부'], label='group_3')
kmf.plot_survival_function()
kmf.fit(durations=group_4['fu_days'], event_observed=group_4['사망여부'], label='group_4')
kmf.plot_survival_function()
plt.ylim(0.5, 1)
plt.xlabel("Days passed")
plt.ylabel("probability of Death")
plt.title("KaplanMeier survival plot")
plt.legend(loc='lower left')
# %%
csv['사망여부'] = csv['사망여부'].fillna(0).astype(int)
csv['alcohol_drinking'] = csv['alcohol_drinking'].fillna(0)
csv['group'] = csv['group'].astype(str)
csv['smoking'] = csv['smoking'].fillna(0).astype(int)

temp = csv.copy()
temp = temp[list(temp.columns[2:14])+['사망여부', 'group', 'fu_days', 'cancer']]
temp['physical_activity'] = temp['physical_activity'].fillna(0)

def apply_fn(x):
    try:
        return x.fillna(x.mean())
    except TypeError:
        return x
        
temp = temp.apply(lambda x: apply_fn(x) ,axis=0)
temp['group'] = temp['group'].astype(str)
# %%
cph = CoxPHFitter()
cph.fit(temp, duration_col='fu_days', event_col='사망여부', 
        formula="age+sex+CCI+group")
cph.print_summary()
cph.plot_partial_effects_on_outcome(covariates='group', values=['1', '2', '3', '4'], plot_baseline=False)
pd.DataFrame(temp.groupby(['group', '사망여부']).size())
# %%
cph.fit(temp, duration_col='fu_days', event_col='cancer', 
        formula="age+sex+CCI+group")
        # formula="age+sex+BMI+smoking+physical_activity+CCI+Hb+HDL+group")
cph.print_summary()
cph.plot_partial_effects_on_outcome(covariates='group', values=['1','2', '3', '4'], plot_baseline=False, 
                                    y='cumulative_hazard')#, alpha=0.7)
pd.DataFrame(temp.groupby(['group', 'cancer']).size())
# %%

# %%

# %%
