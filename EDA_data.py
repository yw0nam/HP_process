# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import cal_percent_group
pd.set_option('display.max_columns', None)

# %%
bx_for_hp = pd.read_csv("./data_for_analysis/hp_bx_2021_10_25.csv", 
                        na_values=np.nan, index_col=0)
bx_for_hp['사망여부'] = bx_for_hp['사망여부'].fillna('N')
print('데이터 N수:',len(bx_for_hp))
pd.DataFrame(bx_for_hp.isna().sum()['age':], columns=['Missing Count'])
# %%
any_csv = pd.read_csv("./data_for_analysis/any_bx_2021_10_25.csv", na_values=np.nan)
any_csv['사망여부'] = any_csv['사망여부'].fillna('N')
print('데이터 N수:',len(any_csv))
pd.DataFrame(any_csv.isna().sum()['age':], columns=['Missing Count'])
# %%
# 1) HP eradicated: HP(+) -> 제균치료(+) -> HP(-)
# 2) HP persistent after eradication Tx: HP(+) -> 제균치료(+) -> HP(+)
# 3) HP persistent: HP(+) -> 제균치료(-) -> HP(+)
# 4) HP natural regression: HP(+) -> 제균치료(-) -> HP(-)

hp_dead_group, hp_dead_percent = cal_percent_group(bx_for_hp, 'group', '사망여부')
any_dead_group, any_dead_percent = cal_percent_group(any_csv, 'group', '사망여부')

dead_percent = pd.DataFrame([hp_dead_percent, any_dead_percent]).T
dead_percent.columns = ['data_bx_hp', 'data_any_bx']
plt.figure();
dead_percent.plot.barh()
plt.gca().set(title='Die percentage each group', xlabel='percentage(%)')
# %%
hp_cancer_group, hp_cancer_percent = cal_percent_group(bx_for_hp, 'group', 'cancer')
any_cancer_group, any_cancer_percent = cal_percent_group(any_csv, 'group', 'cancer')

cancer_percent = pd.DataFrame([hp_cancer_percent, any_cancer_percent]).T
cancer_percent.columns = ['data_bx_hp', 'data_any_bx']
plt.figure();
cancer_percent.plot.barh()
plt.gca().set(title='cancer percentage each group', xlabel='percentage(%)')
# %%
