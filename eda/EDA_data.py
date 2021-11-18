# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import cal_percent_group
import seaborn as sns
pd.set_option('display.max_columns', None)

# %%
bx_for_hp = pd.read_csv("./data_for_analysis/hp_bx.fu365.fu_cdw.csv", 
                        na_values=np.nan, index_col=0)
bx_for_hp['사망여부'] = bx_for_hp['사망여부'].fillna('N')
print('데이터 N수:',len(bx_for_hp))
pd.DataFrame(bx_for_hp.isna().sum()['age':], columns=['Missing Count'])
# %%
any_csv = pd.read_csv("./data_for_analysis/any_bx.fu365.fu_cdw.csv", na_values=np.nan)
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

fig = plt.figure(figsize=(20, 5))
sns.set_style('dark')
area1 = fig.add_subplot(1, 4, 1)
area1.set_title('Group 1 follow up lengths')
area2 = fig.add_subplot(1, 4, 2)
area2.set_title('Group 2 follow up lengths')
area3 = fig.add_subplot(1, 4, 3)
area3.set_title('Group 3 follow up lengths')
area4 = fig.add_subplot(1, 4, 4)
area4.set_title('Group 4 follow up lengths')
sns.histplot(bx_for_hp.query('group == 1')['fu_days'], ax=area1)
sns.histplot(bx_for_hp.query('group == 2')['fu_days'], ax=area2)
sns.histplot(bx_for_hp.query('group == 3')['fu_days'], ax=area3)
sns.histplot(bx_for_hp.query('group == 4')['fu_days'], ax=area4)
plt.show()
# %%
fig = plt.figure(figsize=(20, 5))
sns.set_style('dark')
area1 = fig.add_subplot(1, 4, 1)
area1.set_title('Group 1 follow up lengths')
area2 = fig.add_subplot(1, 4, 2)
area2.set_title('Group 2 follow up lengths')
area3 = fig.add_subplot(1, 4, 3)
area3.set_title('Group 3 follow up lengths')
area4 = fig.add_subplot(1, 4, 4)
area4.set_title('Group 4 follow up lengths')
sns.histplot(any_csv.query('group == 1')['fu_days'], ax=area1)
sns.histplot(any_csv.query('group == 2')['fu_days'], ax=area2)
sns.histplot(any_csv.query('group == 3')['fu_days'], ax=area3)
sns.histplot(any_csv.query('group == 4')['fu_days'], ax=area4)
plt.show()
# %%
bx_for_hp['처방일자'] = pd.to_datetime(bx_for_hp['처방일자'])
bx_for_hp['first_fu'] = pd.to_datetime(bx_for_hp['first_fu'])
bx_for_hp['last_fu'] = pd.to_datetime(bx_for_hp['last_fu'])
bx_for_hp_fu_3 = bx_for_hp.query('last_fu != first_fu')
# %%
bx_for_hp_fu_3['fu_days_2'] = (bx_for_hp_fu_3['last_fu'] -bx_for_hp_fu_3['first_fu']).map(lambda x:x.days)
# %%
bx_for_hp_fu_3.query('fu_days_2 >= 365')['fu_days_2'].hist()
# %%