# %%
from lifelines.plotting import add_at_risk_counts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tableone import TableOne
import warnings
from lifelines import KaplanMeierFitter, NelsonAalenFitter, CoxPHFitter
from lifelines.statistics import logrank_test
warnings.filterwarnings("ignore", category=DeprecationWarning) 
pd.set_option('display.max_columns', None)
# %%
csv = pd.read_csv('../data_with_family_hx/bx_for_hp.cov.fillna_cancer.up_death.final_fu.add_fu.csv')

# %%
# csv['cancer_fu_date'] = csv.apply(lambda x: '2021-10-12' if x['cancer_fu'] == 'N' else x['cancer_fu_date'], axis=1)
# csv['final_fu_death'] = csv.apply(lambda x: '2021-10-12' if x['사망여부'] == 'N' else x['final_fu_death'], axis=1)
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
csv['EGD'] = csv['EGD'].replace({'WNL': 0, 'CSG': 0, 'LFG':0, 'CAG':1, 'MG':2})
# %%
csv['cancer_fu_duration'] = (csv['cancer_fu_date'] - csv['index_date']).map(lambda x: x.days)
csv['death_fu_duration'] = (csv['final_fu_death'] - csv['index_date']).map(lambda x: x.days)
# %%
results = logrank_test(csv.query('group == 1')['cancer_fu_duration'], csv.query('group == 2')['cancer_fu_duration'],
                       event_observed_A=csv.query('group == 1')['cancer_fu'], 
                       event_observed_B=csv.query('group == 2')['cancer_fu'])
# %%
naf = NelsonAalenFitter()
naf.fit(durations=csv.query('group == 1')['cancer_fu_duration'],
        event_observed=csv.query('group == 1')['cancer_fu'], label='HP persistent')
naf.plot_cumulative_hazard()
naf.fit(durations=csv.query('group == 2')['cancer_fu_duration'],
        event_observed=csv.query('group == 2')['cancer_fu'], label='HP natural regression')
naf.plot_cumulative_hazard()
plt.ylim(0, 0.35)
plt.xlabel("Days passed")
plt.ylabel("cumulative hazard of cancer")
plt.text(0, 0.25, 'Log rank P=%s'%str(round(results.p_value, 4)), va='bottom', in_layout=False)
plt.title("NelsonAalenFitter plot about cancer")
plt.legend(loc='upper left')
# %%
naf.fit(durations=csv.query('group == 1')['cancer_fu_duration'],
        event_observed=csv.query('group == 1')['cancer_fu'], label='HP persistent')
t = naf.plot(ci_show=True, at_risk_counts=True,  ylabel='probability of Cancer')
plt.ylim(0, 0.35)
t.get_legend().remove()
plt.show()
# %%
naf.fit(durations=csv.query('group == 2')['cancer_fu_duration'],
        event_observed=csv.query('group == 2')['cancer_fu'], label='HP natural regression')
t = naf.plot(ci_show=True, at_risk_counts=True,  ylabel='probability of Cancer')
plt.ylim(0, 0.35)
t.get_legend().remove()
plt.show()
# %%
results = logrank_test(csv.query('group == 1')['death_fu_duration'], csv.query('group == 2')['death_fu_duration'],
                       event_observed_A=csv.query('group == 1')['사망여부'], 
                       event_observed_B=csv.query('group == 2')['사망여부'])
# %%
kmf = KaplanMeierFitter() 
kmf.fit(durations=csv.query('group == 1')['death_fu_duration'],
        event_observed=csv.query('group == 1')['사망여부'], label='HP persistent')
kmf.plot_survival_function()
kmf.fit(durations=csv.query('group == 2')['death_fu_duration'],
        event_observed=csv.query('group == 2')['사망여부'], label='HP natural regression')
plt.ylim(0.8, 1)
kmf.plot_survival_function()
plt.text(0, 0.85, 'Log rank P=%s'%str(round(results.p_value, 4)), va='bottom', in_layout=False)
plt.xlabel("Days passed")
plt.ylabel("probability of Death")
plt.title("KaplanMeier survival plot")
plt.legend(loc='lower left')
# %%
kmf.fit(durations=csv.query('group == 1')['death_fu_duration'],
        event_observed=csv.query('group == 1')['사망여부'],  label='HP persistent')
t = kmf.plot(ci_show=True, at_risk_counts=True, ylabel='probability of Death')
plt.ylim(0.8, 1)
t.get_legend().remove()
plt.show()
# %%
kmf.fit(durations=csv.query('group == 2')['death_fu_duration'],
        event_observed=csv.query('group == 2')['사망여부'],  label='HP natural regression')
t = kmf.plot(ci_show=True, at_risk_counts=True, ylabel='probability of Death')
plt.ylim(0.8, 1)
t.get_legend().remove()
plt.show()
# %%
csv['사망여부'] = csv['사망여부'].fillna(0).astype(int)
csv['alcohol_drinking'] = csv['alcohol_drinking'].fillna(0)
csv['group'] = csv['group'].astype(str)
csv['smoking'] = csv['smoking'].fillna(0).astype(int)
temp = csv.copy()
temp = temp[list(temp.columns[2:14])+['사망여부', 'group', 'index_date', 'cancer_fu', 'cancer_fu_date', 'final_fu_death', 'EGD', 'group_merged']]
temp['physical_activity'] = temp['physical_activity'].fillna(0)
# %%
temp['group'] = temp['group'].replace({'3':'1', '4':'2'})
# %%
def apply_fn(x):
    try:
        return x.fillna(x.mean())
    except TypeError:
        return x
        
temp = temp.apply(lambda x: apply_fn(x) ,axis=0)
temp['group'] = temp['group'].astype(int)
# %%
temp['cancer_fu_duration'] = (temp['cancer_fu_date'] - temp['index_date']).map(lambda x: x.days)
temp['death_fu_duration'] = (temp['final_fu_death'] - temp['index_date']).map(lambda x: x.days)
temp['EGD'] = temp['EGD'].astype(int)
# %%
cph = CoxPHFitter()
cph.fit(temp, duration_col='death_fu_duration', event_col='사망여부', 
        formula="age+sex+CCI+EGD+group")
cph.print_summary()
cph.plot_partial_effects_on_outcome(covariates='group', values=[1, 2], plot_baseline=False)
# %%
cph.plot(columns=['group'], hazard_ratios=True)
# %%
cph.fit(temp, duration_col='cancer_fu_duration', event_col='cancer_fu', 
        formula="age+sex+CCI+EGD+group")
cph.print_summary()
cph.plot_partial_effects_on_outcome(covariates='group', values=[1,2], plot_baseline=False, 
                                    y='cumulative_hazard')#, alpha=0.7)
# %%
cph.plot(columns=['sex', 'CCI', 'age', 'EGD', 'group'])

# %%
cph.hazard_ratios_
# %%
cph.l1_ratio
# %%
